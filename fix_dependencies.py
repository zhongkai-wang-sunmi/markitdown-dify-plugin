import re
import sys
import importlib.util

def patch_pydub():
    # 定位 pydub.utils 模块
    try:
        pydub_utils_spec = importlib.util.find_spec('pydub.utils')
        if not pydub_utils_spec or not pydub_utils_spec.origin:
            return False
            
        # 读取文件内容
        with open(pydub_utils_spec.origin, 'r') as f:
            content = f.read()
        
        # 修复无效的转义序列
        fixed_content = content.replace("'([su]([0-9]{1,2})p?) \\(([0-9]{1,2}) bit\\)$'", 
                                       "r'([su]([0-9]{1,2})p?) \\(([0-9]{1,2}) bit\\)$'")
        fixed_content = fixed_content.replace("'([su]([0-9]{1,2})p?)( \\(default\\))?$'", 
                                             "r'([su]([0-9]{1,2})p?)( \\(default\\))?$'")
        fixed_content = fixed_content.replace("'(flt)p?( \\(default\\))?$'", 
                                             "r'(flt)p?( \\(default\\))?$'")
        fixed_content = fixed_content.replace("'(dbl)p?( \\(default\\))?$'", 
                                             "r'(dbl)p?( \\(default\\))?$'")
        
        # 写回修复后的内容
        with open(pydub_utils_spec.origin, 'w') as f:
            f.write(fixed_content)
        
        return True
    except Exception as e:
        print(f"修复 pydub 失败: {e}")
        return False

def patch_youtube_transcript_api():
    try:
        # 尝试定位 youtube_transcript_api 测试模块
        yta_test_spec = importlib.util.find_spec('youtube_transcript_api.test.test_cli')
        if not yta_test_spec or not yta_test_spec.origin:
            return False
            
        # 读取文件内容
        with open(yta_test_spec.origin, 'r') as f:
            content = f.read()
        
        # 修复无效的转义序列
        fixed_content = content.replace('"\\-v1 \\-\\-v2 \\--v3"', 'r"\\-v1 \\-\\-v2 \\--v3"')
        
        # 写回修复后的内容
        with open(yta_test_spec.origin, 'w') as f:
            f.write(fixed_content)
        
        return True
    except Exception as e:
        print(f"修复 youtube_transcript_api 失败: {e}")
        return False

# 应用补丁
patch_pydub()
patch_youtube_transcript_api() 