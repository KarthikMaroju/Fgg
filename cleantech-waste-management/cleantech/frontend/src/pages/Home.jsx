import { Link } from "react-router-dom";
export default function Home() {
  return (<><h1>Cleantech: smarter waste sorting</h1>
    <p>Upload a photo of waste. A MobileNetV2 transfer-learning model predicts its category, with confidence scores and disposal guidance.</p>
    <ul><li>Drag-and-drop image classification</li><li>Per-category disposal and recycling tips</li><li>Searchable history and live statistics</li></ul>
    <Link className="btn" to="/classify">Classify an image</Link></>);
}
