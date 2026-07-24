import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Layout, Typography, Card, Button } from "antd";

const { Header, Content } = Layout;
const { Title } = Typography;

export default function Sitemaps() {
  const [sitemaps, setSitemaps] = useState([]);
  const navigate = useNavigate();
  useEffect(() => {
    const fetchSitemaps = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/sitemaps");
        const data = await response.json();
        console.log(data);
        setSitemaps(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchSitemaps();
  }, []);

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
        <Title level={3}>Stored Sitemaps</Title>

        {sitemaps.length === 0 ? (
          <p>No sitemaps found.</p>
        ) : (
          sitemaps.map((sitemap) => (
            <Card
              key={sitemap.id}
              style={{ marginBottom: 20 }}
            >
              <Title level={5}>{sitemap.url}</Title>

              <Button
                type="primary"
                onClick={() => navigate(`/urls/${sitemap.id}`)}
              >
                View URLs
              </Button>
            </Card>
          ))
        )}
      </Content>
    </Layout>
  );
}