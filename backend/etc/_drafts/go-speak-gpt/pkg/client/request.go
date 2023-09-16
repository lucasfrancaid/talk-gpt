package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/lucasfrancaid/speak-gpt/internal/pkg/openai"
)

type Client struct {
	*http.Client
}

func NewClient() Client {
	return Client{&http.Client{}}
}

func (c *Client) Jsonify(data any) *bytes.Buffer {
	j, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	return bytes.NewBuffer(j)
}

func (c *Client) NewRequest(method string, route string, body *bytes.Buffer) *http.Request {
	sdk := openai.NewOpenAI()

	url := sdk.ApiUrl + route
	req, err := http.NewRequest(method, url, body)
	if err != nil {
		panic(err)
	}

	fmt.Println(method, url)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+sdk.ApiKey)
	req.Header.Set("OpenAI-Organization", sdk.ApiOrg)

	return req
}
