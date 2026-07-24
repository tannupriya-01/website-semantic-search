import { Routes, Route } from "react-router-dom";

import Dashboard from "./assets/pages/Dashboard";
import Sitemaps from "./assets/pages/sitemap";
import Urls from "./assets/pages/Urls";
import PageViewer from "./assets/pages/PageViewer";
import Search from "./assets/pages/Search";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      {/* <Route path="/sitemaps" element={<Sitemaps />} /> */}
      <Route path="/urls/:sitemapId" element={<Urls />} />
      {/* <Route path="/pages/:pageId" element={<PageViewer />} /> */}
      <Route path="/search" element={<Search />} />
    </Routes>
  );
}

export default App;