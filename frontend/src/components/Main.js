import React, { useState, useEffect, useContext } from "react";
import FilesList from "./subcomponent/FilesList";
import Header from "./subcomponent/Header";
import api from "../service/Api";
import UpdateFiles from "./subcomponent/UpdateFiles";

function Main() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({});
  const [parentId, setParentId] = useState("");
  const [profileInfo, setProfileInfo] = useState({});
  const url = `/api/v1/files/`;

  const getFilesAndProfileData = async () => {
    const requested_data = await api.request("get", `/api/v1/files/`);
    const profile_data = await api.request("get", `/api/v1/users/me/`);
    setData(requested_data.data);
    setProfileInfo(profile_data.data);
    setLoading(false);
  };

  useEffect((_) => {
    getFilesAndProfileData();
  }, []);

  if (loading) {
    return <div>Loading ...</div>;
  }
  return (
    <div>
      <Header profile={profileInfo} setData={setData} parentId={parentId} />
      {data ? (
        <FilesList
          url={url}
          files={data}
          setData={setData}
          parentId={parentId}
          setParentId={setParentId}
        />
      ) : (
        "No files have been uploaded yet"
      )}
    </div>
  );
}

export default Main;
