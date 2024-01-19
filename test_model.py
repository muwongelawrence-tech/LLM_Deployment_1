import httpx
import asyncio

async def main():
    async with httpx.AsyncClient(base_url='http://localhost:3000',timeout=30) as client:
        async with client.stream('POST', '/generate', 
        json = {'prompt': '''
        what is the difference of covid and fever?
        Definition: Fever is a symptom, not a disease. It is an elevation of body
       temperature above the normal range, which is typically around 98.6°F (37°C).
       Causes: Fever can result from various underlying causes, including infections 
      (such as viral or bacterial infections), inflammatory conditions, certain
       medications, heat-related illnesses, or other medical conditions.
      Symptoms: In addition to an increased body temperature, common symptoms of fever may
      include sweating, chills, headache, muscle aches, and fatigue.
      Treatment: Treatment for fever often involves addressing the underlying cause. Over-the-counter medications like acetaminophen (Tylenol) or ibuprofen may be used to alleviate discomfort and lower fever, but they do not treat the root cause.
      In summary, COVID-19 is a specific infectious disease caused by the SARS-CoV-2 virus, and fever is a symptom that can be associated with various illnesses, including COVID-19. While fever is a common symptom of COVID-19, not everyone with a fever has COVID-19, and COVID-19 can present with a range of symptoms beyond fever. If someone experiences symptoms suggestive of COVID-19, testing and consultation with healthcare professionals are essential for accurate diagnosis and appropriate management.
        ''',
        "stream": True }) as it:
            async for chunk in it.aiter_text():
                print(chunk, flush=True, end='')

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())


