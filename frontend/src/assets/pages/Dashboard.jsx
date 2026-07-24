import { useState , useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { Layout, Typography, Input, Button, Card , Drawer , List } from "antd";
import "../../App.css";

const { Header, Content } = Layout;
const { Title } = Typography;

export default function Dashboard() {
  const [sitemapUrl, setSitemapUrl] = useState("");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [sitemaps, setSitemaps] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const fetchSitemaps = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/sitemaps");

    if (!response.ok) {
      throw new Error("Failed to fetch sitemaps");
    }

    const data = await response.json();

    setSitemaps(data);
    setDrawerOpen(true);
  } 
  catch (error) {
    console.error(error);
    alert("Failed to fetch sitemaps");
  }
};

  const handleAdd = async () => {
    if (!sitemapUrl.trim()) {
      alert("Please enter a website URL");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/scrape", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          website: sitemapUrl,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to scrape website");
      }

      const data = await response.json();
      console.log(data);
      await fetchSitemaps();
      setSitemapUrl("");
    } 
    catch (error) {
      console.error(error);
      alert("Failed to call API");
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          color: "white",
          fontSize: "22px",
          fontWeight: "bold",
        }}
      >
        Website Scraper Dashboard
      </Header>

      <Content
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "40px",
        }}
      >
        <Card style={{ width: 600 }}>
          <Title level={3}>Add Sitemap</Title>

          <Input
            placeholder="Enter Sitemap URL"
            value={sitemapUrl}
            onChange={(e) => setSitemapUrl(e.target.value)}
            style={{ marginBottom: 20 }}
          />

          <Button
            type="primary"
            onClick={handleAdd}
            loading={loading}
            block
          >
            Add
          </Button>

          <Button
            style={{ marginTop: 12 }}
            onClick={() => navigate("/search")}
            block
          >
            Search Content
          </Button>

          <Button
            style={{ marginTop: 12 }}
            onClick={fetchSitemaps}
            block
          >
            View Sitemaps
          </Button>
        </Card>
      </Content>
      <Drawer
        title="Available Sitemaps"
        placement="right"
        width={400}
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
      <List
        bordered
        dataSource={sitemaps}
        renderItem={(item) => (
            <List.Item
                style={{ cursor: "pointer" }}
                onClick={() => {
                  setDrawerOpen(false);
                  navigate(`/urls/${item.id}`);
                }}
            >
              {item.url}
            </List.Item>
        )}
      />
      </Drawer>
    </Layout>
  );
}