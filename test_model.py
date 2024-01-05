
import requests

response = requests.post(
   "http://0.0.0.0:3000/translate",
   headers={
      "accept": "text/plain",
      "Content-Type": "text/plain",
   },
   data=''' 
   Once upon a time in a small, impoverished village, there lived a young boy named Alex. His childhood was marked by struggle and hardship, as the village faced economic challenges and scarce resources. Alex's parents worked tirelessly to make ends meet, but life was tough, and dreams seemed like distant fantasies.

From a young age, Alex harbored big dreams. He would often spend his evenings gazing at the stars, imagining a life beyond the confines of their humble village. Despite the adversity, he possessed an unyielding spirit and a determination to change his circumstances.

As the years passed, Alex faced numerous challenges. He had to walk several miles to the nearest school, often with an empty stomach, as the family's financial struggles persisted. Yet, his thirst for knowledge remained unquenchable. Alex excelled in his studies, fueled by the hope that education could be his ticket to a better life.

One day, a kind teacher named Mrs. Hernandez recognized Alex's potential and took him under her wing. She provided guidance, support, and even arranged for additional learning resources. Alex's academic prowess blossomed, and he became a source of inspiration for his peers.

Despite the odds, Alex secured a scholarship to a prestigious university in the city. Leaving his village for the first time, he was filled with a mix of excitement and anxiety. The city presented new challenges, but Alex's resilience and determination remained unwavering.

In university, Alex discovered a passion for engineering. He dedicated himself to his studies, worked part-time jobs to support himself, and sought out internships to gain practical experience. His hard work and tenacity paid off when he graduated with honors, earning a degree that seemed like an impossible dream during his early years.

Armed with his newfound knowledge and skills, Alex landed a job at a renowned tech company. His success story became an inspiration, not only to his village but to anyone facing adversity. Alex never forgot his roots and used his success to give back to his community, establishing scholarship programs and mentorship initiatives to support aspiring young minds.

Through grit, determination, and the support of those who believed in him, Alex transformed his life from one of hardship to one of accomplishment. His journey underscored the power of education, perseverance, and the belief that even in the darkest times, a brighter future is possible with unwavering determination.
   ''', # Replace $PROMPT here with your prompt.
)

print(response.text)