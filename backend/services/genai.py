from langchain_community.document_loaders.youtube import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAI
from langchain.chains.summarize import load_summarize_chain
from vertexai.generative_models import GenerativeModel
from tqdm import tqdm
from langchain.prompts import PromptTemplate
import logging
import json



# configure log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiProcessor:
    def __init__(self, model_name, project):
        self.model = VertexAI(model_name=model_name, project=project)
        
    def generate_document_summary(self, documents:list, **args):
        chain_type = "map_reduce" if len(documents) > 10 else "stuff"
        chain = load_summarize_chain(
        llm = self.model, 
        chain_type = chain_type, 
        **args
        )
        return chain.run(documents)
    
    def count_total_tokens(self, docs: list):
        temp_modal = GenerativeModel("gemini-1.0-pro")
        total = 0
        logging.info("Counting total billable characters...")
        
        for doc in tqdm(docs):
            total += temp_modal.count_tokens(doc.page_content).total_billable_characters 
        return total
    

    def get_model(self):
        return self.model


class YoutubeProcessor:
    # Retrieve the full transcript

    def __init__(self, genai_processor: GeminiProcessor):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 0
        )
        self.genai_processor = genai_processor

    def retrieve_youtube_documents(self, video_url: str, verbose = False):
        try:
            # Extract the video ID from the shortened URL
            if "youtu.be" in video_url:
                video_id = video_url.split("/")[-1].split("?")[0]
                complete_url = f"https://www.youtube.com/watch?v={video_id}"
            else:
                video_id = video_url.split("v=")[1].split("&")[0]
                complete_url = f"https://www.youtube.com/watch?v={video_id}"
            loader = YoutubeLoader.from_youtube_url(youtube_url=complete_url, add_video_info=True)
            docs = loader.load()
            logging.info(f"On Load: {type(docs)}")

            result = self.text_splitter.split_documents(docs)
            logging.info(f"{type(result)}")
            logging.info(f"Retrieved documents: {result}")

            author = result[0].metadata['author']
            length = result[0].metadata['length']
            title = result[0].metadata['title']
            total_size = len(result)
            text =result[0].page_content

            total_billable_characters = self.genai_processor.count_total_tokens(result)

            if verbose == True:
                # print(f"{author}\n{length}\n{title}\n{total_size}\n")
                logging.info(f"{author}\n{length}\n{title}\n{total_size}\n{text}\n{total_billable_characters}")
            # return docs
            return result
        
        except IndexError:
            logging.error("Error: Unable to extract video ID from the provided YouTube URL.")
            logging.error(f"YouTube URL: {video_url}")
            return {"error": "Invalid YouTube URL format"}
    
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return {"error": str(e)}     
    
    def find_key_concepts(self, documents: list, sample_size: int = 0, verbose = False):
        logging.info(f"Total number of documents: %d {len(documents)}")
        logging.info(f"Requested group size: %d {sample_size}")
        
        # iterate through all documents of group size N and find key concepts
        
        # if sample_size is None:
        #     sample_size = len(documents)
        #     logging.info(f"Using default group size: %d", sample_size)
        # else:
        #     logging.info(f"Requested group size: %d", sample_size)
        
        # Optimize sample size given no input
        if sample_size is None or sample_size <= 0:
            sample_size = len(documents) // 5
            logging.info(f"Using default group size: %d {sample_size}")
            if verbose: 
                logging.info(f"No sample size specified. Setting number of documents per sample as 5. Sample Size: {sample_size}")
        else:
            logging.info(f"Requested group size: %d {sample_size}")

        if sample_size == 0:
            sample_size = 1  # Ensure sample_size is at least 1

        if sample_size > len(documents):
            logging.error("Group size is larger than the number of documents")
            raise ValueError("Group size is larger than the number of documents")
        
       


        # Find number of documents in each group
        num_docs_per_group = len(documents) // sample_size + (len(documents) % sample_size > 0) 

        # check thresholds for response quality
        if num_docs_per_group > 10:
            raise ValueError("Each group has more than 10 documents and output quality will be degraded significantly. Increase the sample size to reduce the number of documents per group.")
        elif num_docs_per_group > 5:
            logging.warning("Each group has more than 5 documents and output quality is likely to be degraded. Consider increasing the sample_size.")


        # Split documents in in chunks of size num_docs_per_group
        groups = [documents[i:i+num_docs_per_group] for i in range(0, len(documents), num_docs_per_group)]

        batch_concepts = []
        batch_cost = 0
        

        logging.info("Finding key concepts...")
        for group in tqdm(groups):
            # Combine content of documents per group
            group_content = ""

            for doc in group:
                group_content += doc.page_content

            logging.info(f"Group Content: {group_content[:200]}...")
            
            # Prompt for finding concepts
            prompt = PromptTemplate(
                template = """
                Find and define key concepts or terms found in the text:
                {text}


                Respond in the following format as a JSON object without any backticks seperating each concept with a comma:
                {{"concept": "definition", "concept: "definition", ...}}

                """,
                input_variables = ["text"]
                )
            
            # Create a chain to find key concepts
            chain = prompt | self.genai_processor.model

            # Run chain
            output_concept = chain.invoke({"text": group_content})
            batch_concepts.append(output_concept)

            # Post Processing Observation
            if verbose:
                total_input_char = len(group_content)
                total_input_cost = (total_input_char/1000) * 0.000125

                logging.info(f"Running chain on {len(group)} documents")
                logging.info(f"Total input characters: {total_input_char}")
                logging.info(f"Total cost: {total_input_cost}")

                total_output_char = len(output_concept)
                total_output_cost = (total_output_char/1000) * 0.000375

                logging.info(f"Total output characters: {total_output_char}")
                logging.info(f"Total cost: {total_output_cost}")

                batch_cost += total_input_cost + total_output_cost
                logging.info(f"Total group cost: {total_input_cost + total_output_cost}\n")
        
        # Log the content of batch_concepts before conversion
        logging.info(f"batch_concepts: {batch_concepts}")
        
        try:
            # Strip off markdown syntax (```json) from each JSON string
            stripped_batch_concepts = [concept.strip('```json\n').strip('```') for concept in batch_concepts]
            # Remove special characters from the JSON string
            processed_batch_concepts = [concept.replace('\n', '').replace('\t', '') for concept in stripped_batch_concepts]
            # Log the processed batch concepts
            logging.info(f"processed_batch_concepts: {processed_batch_concepts}")
            # Convert Each JSON string in batch_concepts to a Python Dict
            processed_concepts = [json.loads(concept) for concept in processed_batch_concepts if concept.strip()]
        except json.JSONDecodeError as e:
            logging.error("Error converting JSON to Python Dictionary: ", e)
            logging.error("Failed JSON String: ", batch_concepts)
            for concept in batch_concepts:
                logging.error(concept)
            processed_concepts=[]

        logging.info(f"Total Analysis cost: ${batch_cost}")  
        return processed_concepts
