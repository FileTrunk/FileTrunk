import React, { useContext } from "react";
import UpdateFiles from "./UpdateFiles";

const BreadCrumb = ({ setData, setParentId, setPath, path }) => {
  return (
    <div>
      <div className="row my-1">
        <div className="p-2 col">
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb">
              <li className="breadcrumb-item active" aria-current="page">
                <a
                  href="#"
                  onClick={async (e) => {
                    e.preventDefault();
                    setParentId("");
                    setPath([]);
                    await UpdateFiles("", setData);
                  }}
                >
                  /
                </a>
              </li>
              {path.map((folder) => (
                <li
                  className="breadcrumb-item active"
                  key={folder.id}
                  aria-current="page"
                >
                  <a
                    href="#"
                    onClick={async (e) => {
                      e.preventDefault();
                      setParentId(folder.id);
                      const index = path.indexOf(folder);
                      setPath(path.slice(0, index + 1));
                      await UpdateFiles(folder.id, setData);
                    }}
                  >
                    {folder.filename}
                  </a>
                </li>
              ))}
            </ol>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default BreadCrumb;
