ALIASES = {
    'Destroyer' : ['디스트로이어', '디트', '디붕', '디붕이', '분망', '중수'],
    'Warlord' : ['워로드', '워붕', '워붕이', '전태', '고기'],
    'Berserker' : ['버서커', '버섴', '서커', '광기', '비기'],
    'Holy Knight' : ['홀리나이트', '홀리', '홀나'],
    'Slayer' : ['슬레이어', '슬레', '포식', '처단'],
    'Battle Master' : ['배틀마스터', '배마', '배틀', '초심'],
    'Infighter' : ['인파이터', '인파', '충단', '체술'],
    'Soul Master' : ['기공사', '기공', '세맥', '역천'],
    'Lance Master' : ['창술사', '창술', '절정', '절제'],
    'Striker' : ['스트라이커', '스트', '스커', '일격'],
    'Breaker' : ['브레이커', '브레', '브커', '수라', '권왕'],
    'Devil Hunter' : ['데빌헌터', '데빌', '데헌', '강무', '핸건'],
    'Blaster' : ['블래스터', '블래', '포강', '화강'],
    'Hawkeye' : ['호크아이', '호크', '홐', '두동', '죽습'],
    'Scouter' : ['스카우터', '스카', '기술', '유산'],
    'Gunslinger' : ['건슬링어', '건슬', '피메', '사시'],
    'Bard' : ['바드'],
    'Summoner' : ['서머너', '섬너', '퐁퐁', '머너', '상소', '교감'],
    'Arcana' : ['아르카나', '알카', '황제', '황후'],
    'Sorceress' : ['소서리스', '소서', '점화', '환류'],
    'Demonic' : ['데모닉', '모닉', '충', '억'],
    'Blade' : ['블레이드', '블레', '버스트', '잔재'],
    'Reaper' : ['리퍼', '달소', '갈증'],
    'Souleater' : ['소울이터', '소울', '만월', '그믐'],
    'Artist' : ['도화가', '화가', '아가'],
    'Aeromancer' : ['기상술사', '기상'],
}
GET_CLASS = {}
for key, values in ALIASES.items():
    for value in values:
        GET_CLASS[value] = key
        
def get_class(alias: str) -> str:
    return GET_CLASS[alias]