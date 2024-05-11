from enum import StrEnum


class ErrorCode(StrEnum):
    BS101 = "BS101"
    BS102 = "BS102"
    BS103 = "BS103"
    BS104 = "BS104"
    BS105 = "BS105"
    BS106 = "BS106"
    BS107 = "BS107"
    BS108 = "BS108"
    BS109 = "BS109"
    BS110 = "BS110"
    BS111 = "BS111"

    def __init__(self, code):
        self.code = code

    def message(self):
        if self == "BS101":

            return "중복된 데이터를 사용할 수 없습니다."
        elif self == "BS102":
            return "db 저장 에러"
        elif self == "BS103":
            return "해당 사용자를 찾을 수 없습니다."
        elif self == "BS104":
            return "아이디나 비밀번호가 일치하지 않습니다."
        elif self == "BS105":
            return "jwt 토큰 생성 중 오류 발생"
        elif self == "BS106":
            return "로그인이 필요합니다."
        elif self == "BS107":
            return "db 불러오기 에러"
        elif self == "BS108":
            return "jwt 토큰 해독 중 오류 발생"
        elif self == "BS109":
            return "jwt 토큰 타입이 없습니다."
        elif self == "BS110":
            return "비밀번호가 일치하지 않습니다."
        elif self == "BS111":
            return "빈 값은 허용되지 않습니다."
