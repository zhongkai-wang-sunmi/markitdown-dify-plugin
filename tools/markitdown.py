from collections.abc import Generator
from typing import Any
import tempfile
import os

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from markitdown import MarkItDown

class MarkitdownTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        files = tool_parameters.get('files', [])
        
        # Handle empty files array
        if not files:
            yield self.create_text_message("No files provided")
            return

        results = []
        
        # Process each file
        for file in files:
            try:
                file_extension = file.extension if file.extension else '.tmp'
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(file.blob)
                    temp_file_path = temp_file.name
                
                try:
                    md = MarkItDown()
                    result = md.convert(temp_file_path)
                    
                    if result and hasattr(result, 'text_content'):
                        results.append({
                            "filename": file.filename,
                            "content": result.text_content
                        })
                    else:
                        error_msg = f"Conversion failed for file {file.filename}. Result: {result}"
                        yield self.create_text_message(text=error_msg)
                        
                finally:
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                        
            except Exception as e:
                error_msg = f"Error processing file {file.filename}: {str(e)}"
                yield self.create_text_message(text=error_msg)
        
        # Return results based on number of files processed
        if len(results) == 0:
            yield self.create_text_message("No files were successfully processed")
        elif len(results) == 1:
            # For single file, return text content directly
            yield self.create_text_message(results[0]["content"])
        else:
            # For multiple files, combine them with clear separation
            combined_content = ""
            for idx, result in enumerate(results, 1):
                combined_content += f"\n{'='*50}\n"  # Add separator line
                combined_content += f"File {idx}: {result['filename']}\n"  # Add file header
                combined_content += f"{'='*50}\n\n"  # Add separator line
                combined_content += result['content']  # Add file content
                combined_content += "\n\n"  # Add spacing between files
            
            yield self.create_text_message(combined_content.strip())
