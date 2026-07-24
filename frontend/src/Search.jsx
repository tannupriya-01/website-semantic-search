import { useState } from "react";
import { Input, Button, Card, Typography, Space } from "antd";

const { Title, Paragraph } = Typography;

export default function Search() {
    const [query, setQuery] = useState("");
    return (
        <div style={{ padding: "40px" }}>

            <Title level={2}>
                Semantic Search
            </Title>

            <Space.Compact style={{ width: "100%" }}>

                <Input
                    placeholder="Ask anything about the website..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />

                <Button type="primary">
                    Search
                </Button>

            </Space.Compact>

            <Card
                style={{ marginTop: 30 }}
            >

                <Paragraph>
                    Search results will appear here.
                </Paragraph>

            </Card>

        </div>
    );
}