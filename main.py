from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from openai import OpenAI


app = FastAPI()

class PromotionRequest(BaseModel):
    text: str
    image_url: str

@app.post("/generate-hashtags/")
async def generate_hashtags(request: PromotionRequest):


# OpenAI API 키 설정
    api_key= ""

    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=api_key)
    # 사용자 입력 정보
    food_promotion_text = request.text
    
    # GPT-3를 사용하여 관련 해시태그 생성 요청
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        #response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": "I'm going to provide you with a food promotion text in JSON format example, and your response should be in Korean . Your task is to analyze the text and generate hashtags that are relevant to the description. The hashtags should be divided into three categories: 'Specifically Taste Expressions' and 'Situations' and 'Specifically visual'. For each category, please provide exactly Only 3 hashtags that are most relevant and creative"
            },
            {
        "role": "system",
        "content": [
            {"type": "text", "text": "Please analyze the image and recommend Specifically visual that will appeal to consumers"},
            {
            "type": "image_url",
            "image_url": {
                "url": f"{request.image_url}",
            },
            },
        ],
        },
            {
                "role": "user",
                "content": food_promotion_text
            },
            {
                "role": "system",
                "content": """example{
        "맛표현": ["상큼한블루베리","달콤한힐링","여름청량음료"
        ],
        "상황": ["집에서힐링","드라마와함께","여름스무디"
        ],
        "비주얼": ["블루베리토핑","시원한스무디비쥬얼","휘핑크림가득"
        ]
        }"""
            }
        ],
        # tools= data_schema
        # ,  # Removed unnecessary outer brackets
        # # Define the function which needs to be called when the output has received
        # tool_choice={
        #     "name": "data_schema"
        # },
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # GPT 응답에서 텍스트 추출
    response_text = completion.choices[0].message
    # 응답으로부터 해시태그 추출 및 JSON 형식으로 구조화 (가정)
    # 여기서는 GPT-3 응답이 아래와 같은 형식이라고 가정합니다.
    # "맛 표현: #달콤한 #상큼한 #시원한 #여름에좋은 #건강한\n상황: #여름준비 #휴가스낵 #피크닉준비 #오후의간식 #다이어트음료"
    # 이를 파싱하여 JSON 구조로 변환하는 로직을 구현합니다.

    #예시 응답 파싱 (실제 응답 형식에 맞추어 수정 필요)


    return response_text





class searchRequest(BaseModel):
    text: str

@app.post("/search-hashtags/")
async def search_hashtags(request1: searchRequest):

    search_text = request1.text

    api_key= ""

        # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=api_key)
        # 사용자 입력 정보
    hashtag_database = {
        "맥주랑 같이 먹으면 좋은 음식": ["#맥주안주", "#치맥시간", "#펍푸드"],
        "친구들과 바닷가에서 바베큐 파티": ["#비치바베큐", "#해변파티", "#바다뷰와함께"],
        "혼자서 조용히 즐기는 저녁": ["#혼밥의정석", "#조용한저녁", "#나만의시간"],
        "가족과 함께하는 주말 점심": ["#가족외식", "#주말브런치", "#가족시간"],
        "아침에 먹기 좋은 가벼운 식사": ["#모닝루틴", "#건강한아침식사", "#아침에너지"],
        # 맛 표현
        "달콤한 디저트": ["#달콤한행복", "#디저트타임", "#스위트라이프"],
        "매콤한 음식": ["#매운맛에중독", "#매콤달콤", "#화끈한맛"],
        # 상황
        "집에서 즐기는 주말": ["#홈파티", "#집콕주말", "#가족과함께"],
        "카페에서의 오후": ["#카페스타그램", "#커피한잔의여유", "#카페투어"],
        # 비주얼
        "색감이 예쁜 음식": ["#비주얼폭발", "#인스타푸드", "#색감깡패"],
        "플레이팅이 아름다운 요리": ["#아트플레이팅", "#미식가의선택", "#요리의정석"],
        "고소한 아침 식사": ["#고소한빵","공부", "#조용한시간", "#모닝루틴"],
        
        # 비주얼
        "거리의 야경과 함께하는 저녁": ["#야경맛집", "#밤의풍경", "#도시의밤"],
        "가을의 정취를 담은 테이블": ["#가을정취", "#가을식탁", "#계절의맛"],
        "짭짤한 해산물 요리": ["#해산물축제", "#짭짤한맛", "#바다의선물"],
        "입안 가득 퍼지는 매운 맛": ["#매운맛도전", "#매운음식", "#불닭"],
        
        # 상황
        "친구들과 함께하는 홈파티": ["#홈파티", "#친구와함께", "#집들이"],
        "코지한 카페에서의 오후": ["#코지카페", "#카페스타그램", "#오후의휴식"],
        
        # 비주얼
        "길거리에서 발견한 먹거리": ["#길거리음식", "#먹방투어", "#스트리트푸드"],
        "홈메이드 베이킹": ["#홈베이킹", "#수제쿠키", "#베이킹스타그램"],
        
        # 추가 예시
        "모닝 커피와 함께하는 시작": ["#모닝커피", "#아침시작", "#카페인충전"],
        "건강을 생각한 디톡스 주스": ["#디톡스주스", "#건강음료", "#바디클린징"],
        "비 오는 날의 따뜻한 수프": ["#비오는날", "#수프", "#집밥"],
        "여름밤의 시원한 빙수": ["#여름디저트", "#빙수사랑", "#시원한간식"],
        "겨울철 따뜻한 핫초코": ["#핫초코", "#겨울간식", "#따뜻한음료"],
        "가족과 함께하는 바비큐": ["#가족바비큐", "#야외그릴", "#가족모임"],
        "봄꽃과 함께하는 피크닉": ["#봄꽃피크닉", "#야외소풍", "#벚꽃놀이"],
        "가을 밤, 와인 한 잔의 여유": ["#가을와인", "#밤의와인", "#와인러버"],
    }

        
        # GPT-3를 사용하여 관련 해시태그 생성 요청
    completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={ "type": "json_object" },
            #response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content": f"너는 해시태그 데이터 기반 검색 AI야 사용자가 검색어를 입력하면 {hashtag_database}에서 json으로 그 검색어에 알맞는 해시태그 3개를 찾아줘 "
                },
                {
                    "role": "user",
                    "content": search_text
                }
            ],
            # tools= data_schema
            # ,  # Removed unnecessary outer brackets
            # # Define the function which needs to be called when the output has received
            # tool_choice={
            #     "name": "data_schema"
            # },
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # GPT 응답에서 텍스트 추출
    response_text1 = completion.choices[0].message
    return response_text1

@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI application!"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
