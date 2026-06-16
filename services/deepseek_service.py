import requests
import json
from flask import current_app

class DeepSeekService:
    """Service for DeepSeek API integration"""
    
    def __init__(self):
        self.api_key = current_app.config.get('DEEPSEEK_API_KEY')
        self.api_base = 'https://api.deepseek.com/v1'
    
    def diagnose(self, metrics_dict):
        """
        Get AI diagnosis from DeepSeek based on IQA metrics
        
        Args:
            metrics_dict: Dictionary containing IQA metrics
        
        Returns:
            Dictionary with diagnosis results
        """
        # For now, return mock data since API key is not set
        if not self.api_key:
            return self._get_mock_diagnosis(metrics_dict)
        
        try:
            prompt = self._build_prompt(metrics_dict)
            response = self._call_deepseek(prompt)
            return self._parse_response(response)
        except Exception as e:
            # Fall back to mock data on error
            return self._get_mock_diagnosis(metrics_dict)
    
    def _build_prompt(self, metrics_dict):
        """Build prompt for DeepSeek"""
        prompt = f"""
        作为AI医生，请诊断以下图像质量指标：
        
        健康评分: {metrics_dict.get('health_score', 0)}
        清晰度: {metrics_dict.get('sharpness', 0)}
        对比度: {metrics_dict.get('contrast', 0)}
        亮度: {metrics_dict.get('brightness', 0)}
        噪声: {metrics_dict.get('noise', 0)}
        压缩损伤: {metrics_dict.get('compression', 0)}
        
        请提供：
        1. 诊断结果（简要说明问题）
        2. 主要问题列表
        3. 建议的治疗方案
        4. 风险等级（low/medium/high）
        
        返回JSON格式的结果。
        """
        return prompt
    
    def _call_deepseek(self, prompt):
        """Call DeepSeek API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7
        }
        
        response = requests.post(
            f'{self.api_base}/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    def _parse_response(self, response):
        """Parse DeepSeek response"""
        try:
            content = response['choices'][0]['message']['content']
            # Extract JSON from response
            # This is simplified - real implementation would be more robust
            return {
                'diagnosis_text': content,
                'problems': [],
                'recommendations': [],
                'risk_level': 'medium'
            }
        except Exception as e:
            raise Exception(f"Failed to parse DeepSeek response: {str(e)}")
    
    @staticmethod
    def _get_mock_diagnosis(metrics_dict):
        """Return mock diagnosis for testing"""
        health_score = metrics_dict.get('health_score', 0)
        
        if health_score < 50:
            diagnosis_text = "患者存在明显质量问题。图像清晰度严重不足，建议进行超分辨率增强处理。"
            risk_level = "high"
        elif health_score < 70:
            diagnosis_text = "患者图像质量一般。检测到模糊和噪声问题，建议进行去噪和清晰度增强。"
            risk_level = "medium"
        else:
            diagnosis_text = "患者图像质量良好。仅需轻微调整。"
            risk_level = "low"
        
        return {
            'diagnosis_text': diagnosis_text,
            'problems': ["低清晰度", "高噪声" if health_score < 70 else "轻微噪声"],
            'recommendations': ["超分辨率增强", "去噪处理", "色彩校正"],
            'risk_level': risk_level
        }
