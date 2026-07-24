import { useState } from "react";
import { Layout, Typography, AutoComplete, Input, Button, Card, Spin, Tag, Empty, Divider, Space, message, } from "antd";
import "./search.css";

const { Content } = Layout;
const { Title, Text, Paragraph } = Typography;

export default function Search() {
  const [query, setQuery] = useState("");
  const [options, setOptions] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedCards, setExpandedCards] = useState({});

  const highlightText = (text, query) => {
    if (!text || !query) return text;
    const stopWords = new Set(["a", "an", "the", "of", "to", "in", "on", "and" , "are" , "it" , "is"]);
    const words = query
      .trim()
      .split(/\s+/)
      .filter(Boolean)
      .filter((word) => !stopWords.has(word.toLowerCase()))
      .map((word) =>
        word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    if (words.length === 0) return text;
    const regex = new RegExp(`\\b(${words.join("|")})\\b`, "gi");

    return text.split(regex).map((part, index) => {
      const isMatch = words.some(
        (word) => word.toLowerCase() === part.toLowerCase()
      );

      return isMatch ? (
        <mark
          key={index}
          style={{
            backgroundColor: "#ffd54f",
            padding: "0 2px",
            borderRadius: "3px",
          }}
        >
          {part}
        </mark>
      ) : (
        part
      );
    });
  };

  const getSnippet = (text, query) => {
    if (!text) return "";
    if (!query) return text.slice(0, 250) + "...";

    const words = query
      .trim()
      .split(/\s+/)
      .filter(Boolean);

    let firstIndex = -1;

    for (const word of words) {
      const idx = text.toLowerCase().indexOf(word.toLowerCase());

      if (idx !== -1) {
        firstIndex = idx;
        break;
      }
    }

    if (firstIndex === -1) {
      return text.slice(0, 250) + "...";
    }

    const start = Math.max(0, firstIndex - 100);
    const end = Math.min(text.length, firstIndex + 180);

    let snippet = text.substring(start, end);

    if (start > 0) {
      snippet = "... " + snippet;
    }

    if (end < text.length) {
      snippet += " ...";
    }

    return snippet;
  };
  
  const fetchSuggestions = async (value) => {
    setQuery(value);

    if (!value.trim()) {
      setOptions([]);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/suggest?q=${encodeURIComponent(value)}`
      );

      const data = await response.json();
      const formattedOptions = data.suggestions.map((item) => ({
        value: item,
      }));

      setOptions(formattedOptions);
    } catch (error) {
      console.error("Suggestion error:", error);
    }
  };

  const handleSearch = async () => {
    console.log("Searching:", query);

    if (!query.trim()) {
      message.warning("Please enter a search query.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/semantic-search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Search request failed.");
      }

      const data = await response.json();

      console.log("Backend Response:", data);
      console.log(data.results);
      setResults(data.results || []);

      if ((data.results || []).length === 0) {
        message.info("No relevant documents found.");
      }
    } catch (err) {
      console.error(err);

      message.error(
        "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout className="search-page">
      <Content className="search-container">
        <Card className="search-header">
          <Title level={2} className="search-title">
            🔍 Semantic Search
          </Title>

          <Text type="secondary" className="search-subtitle">
            Search across all scraped website content using semantic similarity.
          </Text>

          <Divider />

          <Space.Compact className="search-box">
            <AutoComplete
              style={{ width: "100%" }}
              options={options}
              value={query}
              onSearch={fetchSuggestions}
              onSelect={(value) => setQuery(value)}
            >
              <Input
                size="large"
                placeholder="Search across all scraped content..."
                onPressEnter={handleSearch}
              />
            </AutoComplete>

            <Button
              type="primary"
              size="large"
              loading={loading}
              onClick={handleSearch}
            >
              Search
            </Button>
          </Space.Compact>

          {!loading && results.length > 0 && (
            <div className="search-info">
              <Text strong>
                Query:
              </Text>{" "}
              <Tag color="blue">{query}</Tag>

              <Tag color="green">
                {results.length} Results Found
              </Tag>
            </div>
          )}

          {loading && (
            <div
              style={{
                marginTop: 50,
                textAlign: "center",
              }}
            >
              <Spin size="large" />

              <Paragraph
                style={{
                  marginTop: 15,
                }}
              >
                Searching through embeddings...
              </Paragraph>
            </div>
          )}

          {!loading && results.length === 0 && (
            <div
              style={{
                marginTop: 50,
              }}
            >
              <Empty
                description="No search results yet"
              />
            </div>
          )}

          {!loading && results.length > 0 && (
            <div className="results-grid">
              {results.map((item, index) => (
                  <Card
                    key={index}
                    hoverable
                    className="result-card"
                  >
                    <div className="result-title">
                      {item.title}
                    </div>

                    <div className="result-url">
                      <Space wrap>
                          {item.keywords?.map((word, index) => (
                              <Tag key={index}>
                                  {word}
                              </Tag>
                          ))}
                      </Space>
                      <div
                          style={{
                              marginTop: 10
                          }}
                      >
                          <a
                              href={item.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                  color: "#1677ff",
                                  textDecoration: "underline",
                                  fontSize: "13px",
                                  wordBreak: "break-all"
                              }}
                          >
                              {item.url}
                          </a>
                      </div>
                  </div>
                      <Paragraph>
                        {highlightText(
                          expandedCards[index]
                            ? item.summary
                            : getSnippet(item.summary, query),
                          query
                        )}

                        {item.summary.length > 220 && (
                          <div
                            style={{
                              color: "#1677ff",
                              cursor: "pointer",
                              marginTop: 8,
                              fontWeight: 500
                            }}
                            onClick={() =>
                              setExpandedCards({
                                ...expandedCards,
                                [index]: !expandedCards[index]
                              })
                            }
                          >
                            {expandedCards[index] ? "Show Less" : "Show More"}
                          </div>
                        )}
                    </Paragraph>
                  </Card>
                ))}
              </div>
            )}
        </Card>
      </Content>
    </Layout>
  );
}