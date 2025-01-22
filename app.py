from flask import Flask, render_template, request, jsonify
import requests
import uuid
import json
import re
import os

app = Flask(__name__)

# Configuration for Blackbox AI API
cookies = {
    'sessionId': '60da9ffd-8a45-475a-bff2-3745892f516c',
    '__Host-authjs.csrf-token': '1ef0785ddec27c9769f0f404b85ad85bf9208e924dcdbc163cab86e308274910%7C7bfec46e4faacfa92b3874eb8feb5c0c5c63f635ef0b178c0e526f9d5fd38eb4',
    'intercom-id-jlmqxicb': 'd4a9dec8-fbfb-4b1c-8c85-80d83589ae28',
    'intercom-device-id-jlmqxicb': 'dfcc2489-2b31-49ae-b90d-672f0c5e222f',
    'g_state': '{"i_l":0}',
    '__Secure-authjs.callback-url': 'https%3A%2F%2Fwww.blackbox.ai%2F',
    'intercom-session-jlmqxicb': 'YWljN0lWZmhUN3cwRjN6VXVsQ3hwU2lsVDJSMmJoMlZhSU5OYXBleTl4cTRjMlEvVEVlYmRxcm11TEgyWUhJaS0taTRxZThjVzdVT0RtQ1R0UFJQMDM4dz09--113d684ca9db43ab63697c9d1ecf9c0eb9395ddd',
    '__Secure-authjs.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..9QZZyPhQpiAfzEfK.EntLnYT3YOsiu1XTleiS8LOLuGtNpL-DSstHcgq9lV-MK5tHNOgNHpPxZUHJuH-GohzVLI9g1FTC4fUy_c14pmyop8uuDZqiF80_mRMw7ijBdwHyCqZSfefqQ0HRzqYur7PvlshpNZfa-JJ3-BNz_JZg3eCpLoicBt5m4TXkJR68nkJL6Li33Xg-BpdUjsG6_7pcemp1xlQqDAVS6tHvR5M1WtRDmWtrQGSNoHG5SGfSsFNm5B2mMcjodbvZhPNOZoSEcE_4-5Gxw5dFvMoy1Wv29z5qZ9hOPmsDMh9-uIrvcGLp4wHE245gb4hy3mKoFZF5owjyihkelrDhv2BwFQ3SiiOzejpDAr70sKxpVkHBfzQTnvUdKhivnkWo4DYD-HDd4ZU0djdjjPgFPzqBtoxtQx2o0zxDQ_Cp9fPP9VktA-_lMYsT43Imw9AmeaJI0Iuy0s0ynoDVu6yDT-27dQLhM5ExHLsU8_g5_CXP7YclycOpy2X2cn_pdiVUEoa2GOcAk9WrRHk.pUJbqTcQiDNuGTAF4SvV_w',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://www.blackbox.ai',
    'priority': 'u=1, i',
    'referer': 'https://www.blackbox.ai/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    # Get form data
    data = request.get_json()
    
    # Construct resume sections with comprehensive formatting
    resume_sections = []
    
    if data.get('personal_info'):
        resume_sections.append("CONTACT INFORMATION")
        resume_sections.append(f"{data['personal_info'].get('name', '')}")
        resume_sections.append(f"{data['personal_info'].get('address', '')}")
        resume_sections.append(f"Email: {data['personal_info'].get('email', '')}")
        resume_sections.append(f"Phone: {data['personal_info'].get('phone', '')}")
        resume_sections.append(f"LinkedIn: {data['personal_info'].get('linkedin', '')}")
    
    if data.get('summary'):
        resume_sections.append("\nPROFESSIONAL SUMMARY")
        resume_sections.append(data['summary'])
    
    if data.get('experience'):
        resume_sections.append("\nPROFESSIONAL EXPERIENCE")
        resume_sections.append(data['experience'])
    
    if data.get('education'):
        resume_sections.append("\nEDUCATION")
        resume_sections.append(data['education'])
    
    if data.get('skills'):
        resume_sections.append("\nSKILLS")
        resume_sections.append(data['skills'])
    
    if data.get('certifications'):
        resume_sections.append("\nCERTIFICATIONS")
        resume_sections.append(data['certifications'])
    
    if data.get('awards'):
        resume_sections.append("\nAWARDS & ACHIEVEMENTS")
        resume_sections.append(data['awards'])
    
    if data.get('projects'):
        resume_sections.append("\nRELEVANT PROJECTS")
        resume_sections.append(data['projects'])
    
    if data.get('languages'):
        resume_sections.append("\nLANGUAGES")
        resume_sections.append(data['languages'])
    
    if data.get('volunteer'):
        resume_sections.append("\nVOLUNTEER EXPERIENCE")
        resume_sections.append(data['volunteer'])

    # Updated prompt with comprehensive structure
    template = """Create a professional HTML resume with the following structure:

<div class="resume-header">
    <h1>[Full Name]</h1>
    <div class="contact-details">
        [Address]<br>
        Email: [Email] | Phone: [Phone]<br>
        [LinkedIn if provided]
    </div>
</div>

<div class="resume-section">
    <h2>PROFESSIONAL SUMMARY</h2>
    <p class="summary">[Professional summary with key achievements and goals]</p>
</div>

<div class="resume-section">
    <h2>PROFESSIONAL EXPERIENCE</h2>
    <div class="experience-item">
        [For each position:]
        <div class="title">[Job Title] - [Company Name]</div>
        <div class="date">[Start Date] - [End Date] | [Location]</div>
        <ul>
            [Key responsibilities and achievements as list items]
        </ul>
    </div>
</div>

<div class="resume-section">
    <h2>EDUCATION</h2>
    <div class="education-item">
        [Degree/Program]<br>
        [Institution Name] - [Graduation Year]<br>
        [Honors/GPA if applicable]
    </div>
</div>

<div class="resume-section">
    <h2>TECHNICAL SKILLS</h2>
    <ul class="skills-list">
        [Skills categorized and listed]
    </ul>
</div>

[Optional Sections based on provided data:]
- Certifications
- Awards & Achievements
- Projects
- Languages
- Volunteer Experience

Use the following information to fill in the template:

"""

    requirements = """

Requirements:
1. Create a modern, professional layout
2. Use consistent formatting throughout
3. Highlight key achievements and metrics
4. Use bullet points for better readability
5. Include all provided sections, properly formatted
6. Maintain professional spacing and hierarchy
7. Make contact information easily scannable
8. Format dates and company names consistently"""

    prompt = template + '\n'.join(resume_sections) + requirements

    # Update system message for comprehensive formatting
    json_data = {
        'messages': [{
            'role': 'system',
            'content': 'You are an expert resume writer specializing in modern, professional resume formats. Create a comprehensive resume that highlights the candidate\'s strengths and maintains consistent, clean formatting throughout.'
        }, {
            'role': 'user',
            'content': prompt
        }],
        'id': str(uuid.uuid4()),
        'previewToken': None,
        'userId': None,
        'codeModelMode': False,
        'agentMode': {},
        'trendingAgentMode': {},
        'isMicMode': False,
        'userSystemPrompt': None,
        'maxTokens': 4096,
        'playgroundTopP': 0.9,
        'playgroundTemperature': 0.5,
        'isChromeExt': False,
        'githubToken': None,
        'clickedAnswer2': False,
        'clickedAnswer3': False,
        'clickedForceWebSearch': False,
        'visitFromDelta': False,
        'mobileClient': False,
        'userSelectedModel': '',
        'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
    }

    try:
        response = requests.post(
            'https://www.blackbox.ai/api/chat',
            cookies=cookies,
            headers=headers,
            json=json_data,
            timeout=30
        )
        
        if response.status_code == 200:
            resume_text = response.text.strip()
            
            # Clean up the response text
            # Remove everything before the first HTML tag
            cleaned_text = re.sub(r'^.*?<', '<', resume_text, flags=re.DOTALL)
            
            # Remove explanation and code block markers at the end
            cleaned_text = re.sub(r'```.*?$', '', cleaned_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'### Explanation.*?$', '', cleaned_text, flags=re.DOTALL)
            
            # Remove any remaining markdown code block markers
            cleaned_text = cleaned_text.replace('```html', '').replace('```', '')
            
            if cleaned_text:
                return jsonify({
                    'success': True, 
                    'resume': cleaned_text.strip()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Empty response after cleaning'
                })
        else:
            print("API Error Status:", response.status_code)
            print("API Error Response:", response.text)
            return jsonify({
                'success': False, 
                'error': f'API request failed with status code {response.status_code}',
                'response_text': response.text
            })
    
    except Exception as e:
        print("Exception Type:", type(e).__name__)
        print("Exception Details:", str(e))
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 