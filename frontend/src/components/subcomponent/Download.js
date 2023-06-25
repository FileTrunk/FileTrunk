import React from "react";
import download from "./pictures/download.png";
import api from "../../service/Api";

const Download = ({ file_id, url, parentId, setData }) => {
  const onDownload = async () => {
    await api.request("get", `${url}file-load/${file_id}/`).then((data) => {
      window.location.href = `${url}download/?token=${data.token}`;
      //"http://127.0.0.1:8000" +
      // Remove when dockerize
    });
  };
  return (
    <div>
      <img
        src={download}
        alt="Download"
        className="icon d-flex align-items-center"
        onClick={(e) => onDownload()}
      />
    </div>
  );
};

export default Download;
