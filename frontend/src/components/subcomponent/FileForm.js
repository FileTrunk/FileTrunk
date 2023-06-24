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
};import { useState, useEffect } from "react";
import Delete from "./Delete";
import Download from "./Download";
import folder_icon from "./pictures/folder_icon.jpg";
import file_icon from "./pictures/file_icon.png";
import UpdateFiles from "./UpdateFiles";
import BreadCrumb from "./BreadCrumb";
import Share from "./Share";
import api from "../../service/Api";

const FilesList = ({ files, url, parentId, setData, setParentId }) => {
  const [path, setPath] = useState([]);
  const [time, setTime] = useState(1);
  const [link_for_sharing, setShareLink] = useState(false);
  const [file_id, setFileIdState] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      UpdateFiles(parentId, setData);
    }, 20000);
    return () => {
      clearInterval(interval);
    };
  }, [path, parentId]);

  const onShare = async () => {
    const post_info = {
      time: parseInt(time),
      file_id: file_id,
    };
    await api
      .request("post", `${url}share-load/`, post_info, {
        "Content-Type": "application/json",
      })
      .then((response) => {
        const share_link_token = response.data.share_link_token;
        setShareLink(window.location.origin + `/share/${share_link_token}`);
      });
  };

  const onDelete = async () => {
    await api
      .request("delete", `${url}share-load/${file_id}`)
      .then((response) => {
        alert("All links connected to this file have been disabled");
      });
  };

  const FolderForward = async (object) => {
    setParentId(object.id);

    const arr = path;
    arr.push(object);
    setPath(arr);

    await UpdateFiles(object.id, setData);
  };

  const getNormalDate = (string) => {
    const date = new Date(string);
    return date.toUTCString();
  };

  return (
    <div className="container w-50">
      <BreadCrumb
        setData={setData}
        setParentId={setParentId}
        setPath={setPath}
        path={path}
      />
      <div className="row">
        <div className="p-1 col">
          {files.length > 0 ? (
            <table className="table table-bordered">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Updated At</th>
                  <th>Size</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {files.map((object) => (
                  <tr key={object.id}>
                    <td className="text-center align-middle">
                      {!object.is_folder ? (
                        <img alt="fileicon" className="icon" src={file_icon} />
                      ) : (
                        <img
                          className="icon"
                          alt="foldericon"
                          src={folder_icon}
                        />
                      )}
                    </td>
                    <td className="text-center align-middle">
                      {object.is_folder ? (
                        <h6>
                          <a
                            href="#"
                            onClick={async (e) => {
                              e.preventDefault();
                              await FolderForward(object);
                            }}
                          >
                            {object.filename}
                          </a>
                        </h6>
                      ) : (
                        <h6>{`${object.filename}.${object.file_type}`}</h6>
                      )}
                    </td>
                    <td className="text-center align-middle">
                      <h6>{getNormalDate(object.updated_at)}</h6>
                    </td>
                    <td className="text-center align-middle">
                      <h6>{Math.ceil(object.file_size * 100) / 100} MB</h6>
                    </td>
                    <td className="d-flex flex-row border-bottom-0 justify-content-center vertical-align">
                      <Delete
                        file_id={object.id}
                        setData={setData}
                        url={url}
                        parentId={parentId}
                      />
                      {!object.is_folder && (
                        <Download file_id={object.id} url={url} />
                      )}
                      {!object.is_folder && (
                        <Share
                          object_id={object.id}
                          link_for_sharing={link_for_sharing}
                          setTime={setTime}
                          setShareLink={setShareLink}
                          setFileIdState={setFileIdState}
                          onDelete={onDelete}
                          onShare={onShare}
                          time={time}
                        />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <h2>No files in this folder yet</h2>
          )}
        </div>
      </div>
    </div>
  );
};

export default FilesList;


export default FileForm;
