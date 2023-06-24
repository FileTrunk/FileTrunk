import { useState } from "react";
import api from "../../service/Api";
import UpdateFiles from "./UpdateFiles";

const FileForm = ({ parentId, setData }) => {
  const [file, setFile] = useState(null);
  const [folder, setFoldername] = useState("");

  const onFolderSubmit = async () => {
    if (!folder.length) {
      alert("Enter folder name!");
      return;
    }
    const post_info = {
      filename: folder,
      is_folder: true,
      parent_id: parentId,
    };
    const res = await api.request("post", `/api/v1/files/`, post_info, {
      "Content-Type": "application/json",
    });
    if (res) {
      if (res.data.message === "Success") {
        await UpdateFiles(parentId, setData);
      }
    }
  };

  const onFileSubmit = async () => {
    let ext;
    let name;
    const file_size = Math.ceil(file.size / 10000) / 100;
    if (!file) {
      alert("Choose some file to upload!");
      return;
    }
    if (file_size > 100) {
      alert("Your file takes too much place!");
      return;
    }
    const fullFilename = file.name.split("").reverse().join("").split(".");
    ext = fullFilename[0].split("").reverse().join("");
    name = fullFilename.slice(1).join(".").split("").reverse().join("");
    const form_data = new FormData();
    form_data.append("storaged_file", file);
    form_data.append("filename", name);
    form_data.append("file_type", ext);
    form_data.append("file_size", file_size);
    if (parentId !== "") {
      form_data.append("parent_id", parentId);
    }
    const res = await api.request(
      "post",
      `/api/v1/files/file-load/`,
      form_data,
      { "Content-Type": "multipart/form-data" }
    );
    if (res.data.message === "Success") {
      await UpdateFiles(parentId, setData);
    }
  };

  return (
    <div className="container">
      <div className="row">
        <div className="p-2 col">
          <button
            type="button"
            className="btn btn-primary"
            data-toggle="modal"
            data-target="#folderCreation"
          >
            Create folder
          </button>
        </div>
        <div
          id="folderCreation"
          className="modal fade"
          tabIndex="-1"
          role="dialog"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="folderCreationLabel">
                  Create Folder
                </h5>
                <button
                  type="button"
                  className="close"
                  data-dismiss="modal"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div className="modal-body">
                <form>
                  <div className="mb-3">
                    <input
                      type="text"
                      className="form-control"
                      name="filename"
                      value={folder}
                      onChange={(e) => setFoldername(e.target.value)}
                    />
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  data-dismiss="modal"
                >
                  Close
                </button>
                <button
                  className="btn btn-primary"
                  data-dismiss="modal"
                  onClick={(e) => {
                    e.preventDefault(e);
                    onFolderSubmit();
                  }}
                >
                  Create!
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="p-2 col">
          <button
            type="button"
            className="btn btn-primary ms-1"
            data-toggle="modal"
            data-target="#fileCreation"
          >
            Upload File
          </button>
        </div>
        <div
          id="fileCreation"
          className="modal fade"
          tabIndex="-1"
          role="dialog"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="fileCreationLabel">
                  Upload File
                </h5>
                <button
                  type="button"
                  className="close"
                  data-dismiss="modal"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div className="modal-body">
                <form>
                  <div className="mb-2 w-25 float-start">
                    <input
                      type="file"
                      onChange={(e) => setFile(e.target.files[0])}
                    />
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  data-dismiss="modal"
                >
                  Close
                </button>
                <button
                  className="btn btn-primary"
                  data-dismiss="modal"
                  onClick={(e) => {
                    e.preventDefault(e);
                    onFileSubmit();
                  }}
                >
                  Upload!
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileForm;
