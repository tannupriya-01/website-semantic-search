import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Layout, Typography, Card, Spin } from "antd";
import ReactMarkdown from "react-markdown";
import "github-markdown-css/github-markdown.css";

const { Header, Content } = Layout;
const { Title } = Typography;

export default function PageViewer() {
  const { pageId } = useParams();

  const [page, setPage] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPage = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/pages/${pageId}`
        );

        const data = await response.json();
        console.log(data);
        console.log(data.content);

        console.log(data);

        setPage(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchPage();
  }, [pageId]);

  if (loading) {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <Content
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Spin size="large" />
        </Content>
      </Layout>
    );
  }

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          color: "white",
          fontSize: 24,
          fontWeight: "bold",
        }}
      >
        Website Scraper Dashboard
      </Header>

      <Content style={{ padding: 40 }}>
        <Title level={3}>Page Content</Title>

        <Card>
          <Title level={5}>{page.url}</Title>

          <div className="markdown-body">
            <ReactMarkdown>
                {page.content || "No content available."}
            </ReactMarkdown>
          </div>
        </Card>
      </Content>
    </Layout>
  );
}