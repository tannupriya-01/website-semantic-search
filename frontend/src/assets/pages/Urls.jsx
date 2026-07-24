import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Layout, Typography, Table, Button, Modal } from "antd";
import ReactMarkdown from "react-markdown";

const { Header, Content } = Layout;
const { Title } = Typography;

export default function Urls() {
  const { sitemapId } = useParams();
  const navigate = useNavigate();

  const [urls, setUrls] = useState([]);
  const [open, setOpen] = useState(false);
  const [pageContent, setPageContent] = useState("");
  const [pageUrl, setPageUrl] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/sitemaps/${sitemapId}/urls`)
      .then((response) => response.json())
      .then((data) => {
        setUrls(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [sitemapId]);
  
  const viewContent = async (pageId) => {
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/pages/${pageId}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch page content");
      }
      const data = await response.json();
      setPageContent(data.content);
      setPageUrl(data.url);
      setOpen(true);
    }
    catch (error) {
      console.error(error);
      alert("Failed to fetch page content");
    } 
    finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
    },
    {
      title: "URL",
      dataIndex: "url",
      key: "url",
    },
    {
      title: "Action",
      key: "action",
      width: 180,
      render: (_, record) => (
        <Button
          type="primary"
          onClick={() => viewContent(record.id)}
        >
          View Content
        </Button>
      ),
    },
  ];

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

      <Content style={{ padding: 40 }}>
        <Title level={3}>Stored URLs</Title>

        <Table
          rowKey="id"
          columns={columns}
          dataSource={urls}
          pagination={{ pageSize: 10 }}
        />
      </Content>

      <Modal
        title={pageUrl}
        open={open}
        onCancel={() => setOpen(false)}
        footer={null}
        width={1000}
      >
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="markdown-body">
            <ReactMarkdown>
              {pageContent}
            </ReactMarkdown>
          </div>
        )}
      </Modal>
    </Layout>
  );
}