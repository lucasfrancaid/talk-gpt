package openai

type OpenAI struct {
	ApiUrl string
	ApiKey string
	ApiOrg string
}

func NewOpenAI() OpenAI {
	return OpenAI{
		ApiUrl: "https://api.openai.com/v1",
		ApiKey: "OPENAI_KEY",
		ApiOrg: "OPENAI_ORG",
	}
}
