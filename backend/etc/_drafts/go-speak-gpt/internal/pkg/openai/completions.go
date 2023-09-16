package openai

type CompletionsRequest struct {
	Model       string  `json:"model"`
	Prompt      string  `json:"prompt"`
	Temperature float32 `json:"temperature"`
	MaxTokens   int16   `json:"max_tokens"`
}

func NewCompletionsRequest(prompt string) CompletionsRequest {
	promptCtx := "The following is a conversation with an AI English Teacher. The AI English Teacher should correct me when I make a wrong sentence explaining what is wrong and how should be, and should nock conversations about any topic I choose. \n"
	return CompletionsRequest{
		Model:       "text-davinci-003",
		Prompt:      promptCtx + prompt,
		Temperature: float32(0),
		MaxTokens:   100,
	}
}
