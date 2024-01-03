import asyncio
import httpx


# with httpx.Client(base_url='http://localhost:3000') as client:
#     print(
#         client.post('/v1/generate',
#                     json={
#                         'prompt': 'What are Large Language Models?',
#                         'sampling_params': {
#                             'temperature': 0.73
#                         },
#                         "stream": False
#                     }).content.decode())

async def generate():
    async with httpx.AsyncClient(base_url='http://localhost:3000') as client:
        async with client.stream('POST', '/v1/generate',
                                 json={
                                     'prompt': 'What are Large Language Models?',
                                     'sampling_params': {
                                         'temperature': 0.73
                                     },
                                     "stream": True
                                 }) as it:
            async for chunk in it.aiter_text():
                print(chunk, flush=True, end='')

# Run the event loop
if __name__ == "__main__":
    asyncio.run(generate())