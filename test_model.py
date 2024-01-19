import httpx
import asyncio

async def main():
    async with httpx.AsyncClient(base_url='http://localhost:3000',timeout=30) as client:
        async with client.stream('POST', '/generate', 
        json = {'prompt': 'what is the difference of covid and fever?',
        "stream": True }) as it:
            async for chunk in it.aiter_text():
                print(chunk, flush=True, end='')

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())


