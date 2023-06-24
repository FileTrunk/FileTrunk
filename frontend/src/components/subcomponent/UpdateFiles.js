import api from "../../service/Api";

const UpdateFiles = async (parentId, setData) => {
  const new_files = await api.request("get", `/api/v1/files/${parentId}`);
  setData(new_files.data);
};

export default UpdateFiles;
