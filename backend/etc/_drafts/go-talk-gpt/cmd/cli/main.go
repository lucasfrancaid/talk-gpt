package main

import (
	"fmt"
	"io"
	"net/http"

	"github.com/lucasfrancaid/talk-gpt/internal/pkg/openai"
	"github.com/lucasfrancaid/talk-gpt/pkg/client"
)

func main() {
	// res := completions()
	res := chatCompletions()

	body, err := io.ReadAll(res.Body)
	if err != nil {
		panic(err)
	}

	fmt.Println("Status Code:", res.StatusCode)
	fmt.Println("Headers:", res.Header)
	fmt.Println("Body:", string(body))
}

func completions() *http.Response {
	prompt := "Hi, my name is Lucas! I'm 27 old and I work with Software Development. I want to improve my english to get a new job, could you help me to do it?"
	data := openai.NewCompletionsRequest(prompt)

	c := client.NewClient()
	req := c.NewRequest(http.MethodPost, "/completions", c.Jsonify(data))
	res, err := c.Do(req)
	if err != nil {
		panic(err)
	}
	return res
}

func chatCompletions() *http.Response {
	msg := openai.ChatCompletionsMessage{
		Role:    "user",
		Content: "Hi, my name is Lucas! I'm 27 old and I work with Software Development. I want to improve my english to get a new job, could you help me to do it?",
	}
	msgs := []openai.ChatCompletionsMessage{msg}
	data := openai.NewChatCompletionsRequest(msgs)

	c := client.NewClient()
	req := c.NewRequest(http.MethodPost, "/chat/completions", c.Jsonify(data))
	res, err := c.Do(req)
	if err != nil {
		panic(err)
	}
	return res
}
