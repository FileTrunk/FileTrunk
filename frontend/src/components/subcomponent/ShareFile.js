import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import loading_gif from "./pictures/loading.gif";
import api from "../../service/Api";

const ShareFile = () => {
  const { token } = useParams();
  const [download, setDownload] = useState(true);
  const startDownload = async () => {
    window.location.href = `/api/v1/files/share-load/${token}`;
    setDownload(false);
  };
  useEffect(() => {
    startDownload();
  }, []);
  if (download) {
    return (
      <div>
        <h1>Download file</h1>
        <img src={loading_gif} alt="Loading..." className="big-icon" />
      </div>
    );
  }
  return (
    <div>
      <h1>File download must have started</h1>
      <h1>If download haven't started toggle it manually</h1>
      <button
        className="btn btn-primary"
        onClick={() => {
          startDownload();
        }}
      >
        Download
      </button>
    </div>
  );
};

export default ShareFile;
