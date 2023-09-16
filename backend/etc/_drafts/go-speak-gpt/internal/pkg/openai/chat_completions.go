package openai

type ChatCompletionsMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ChatCompletionsRequest struct {
	Model       string                   `json:"model"`
	Messages    []ChatCompletionsMessage `json:"messages"`
	Temperature float32                  `json:"temperature"`
	MaxTokens   int16                    `json:"max_tokens"`
}

func NewChatCompletionsRequest(messages []ChatCompletionsMessage) ChatCompletionsRequest {
	return ChatCompletionsRequest{
		Model:       "gpt-3.5-turbo",
		Messages:    messages,
		Temperature: float32(0.7),
		MaxTokens:   100,
	}
}
