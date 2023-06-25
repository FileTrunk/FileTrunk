import React from "react";
import delete_ic from "./pictures/delete.png";
import api from "../../service/Api";
import UpdateFiles from "./UpdateFiles";

const Delete = ({ file_id, url, setData, parentId }) => {
  const onDelete = async () => {
    const isSure = window.confirm(
      "Are you sure you want to delete this resource?"
    );
    if (!isSure) {
      return;
    }
    const res = await api.request("delete", `${url}${file_id}/`);
    if (res.data.message === "Success") {
      await UpdateFiles(parentId, setData);
    }
  };
  return (
    <div>
      <img
        src={delete_ic}
        alt="Delete"
        className="icon d-flex align-items-start"
        onClick={(e) => onDelete()}
      />
    </div>
  );
};

export default Delete;
