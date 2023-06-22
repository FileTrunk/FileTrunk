import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../service/Api";
import Logout from "./subcomponent/Logout";
import loading_icon from "./subcomponent/pictures/loading.gif";
import profile_bg from "./subcomponent/pictures/profile-bg.jpg";
import { Doughnut } from "react-chartjs-2";

function Profile({ setIfAuthorized }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({});
  const [stats, setStats] = useState({});
  const [loading_stats, setLoadingStats] = useState(true);
  const [doughnut, setDoughnut] = useState({});

  const getStats = async () => {
    const response = await api.request("get", `/api/v1/users/user-stats/`);
    setStats(response.data);
    let randomColors = [];
    for (
      let i = 0;
      i < Object.keys(response.data.files_ext_distribution).length;
      i++
    ) {
      let randomColor = Math.floor(Math.random() * 16777215).toString(16);
      randomColors.push("#" + randomColor);
    }
    setDoughnut({
      labels: Object.keys(response.data.files_ext_distribution),
      datasets: [
        {
          label: "# of Votes",
          data: Object.values(response.data.files_ext_distribution),
          backgroundColor: randomColors,
          borderWidth: 1,
        },
      ],
    });

    setLoadingStats(false);
  };

  const getData = async () => {
    const response = await api.request("get", `/api/v1/users/me/`);
    setData(response.data);
    setLoading(false);
  };

  useEffect((_) => {
    getData();
  }, []);

  useEffect((_) => {
    getStats();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      getStats();
    }, 20000);
    return () => {
      clearInterval(interval);
    };
  }, [loading]);

  if (loading) {
    return <div>Loading ...</div>;
  }
  return (
    <div className="d-flex justify-content-center col-md-12">
      <div className="col-md-6">
        <div className="card">
          <img className="card-img-top" src={profile_bg} alt="Card image cap" />
          <div className="card-body little-profile text-center">
            <div className="col-md-12">
              <div className="pro-img">
                <img src={data.picture} alt={`${data.first_name}'s avatar`} />
              </div>
              <h3 className="m-b-0">
                {data.first_name} {data.last_name}
              </h3>
            </div>
            <div className="d-flex flex-row">
              <div className="col-md-6">
                <h3 className="m-b-0">
                  Files on storage:{" "}
                  {!loading_stats ? stats.number_of_files : "Loading..."}
                </h3>
                <h3 className="m-b-0">
                  Used storage place:{" "}
                  {!loading_stats
                    ? Math.floor(stats.used_storage * 100) / 100 + " MB"
                    : "Loading..."}
                </h3>
                <Link
                  className="m-t-10 waves-effect waves-dark btn btn-primary btn-md btn-rounded"
                  data-abc="true"
                  to="/files"
                >
                  My Files
                </Link>
                <p>
                  <Logout setIfAuthorized={setIfAuthorized} />
                </p>
              </div>
              <div className="col-md-6">
                {loading_stats ? (
                  <img className="loading-icon" src={loading_icon} />
                ) : (
                  <div>
                    {stats.number_of_files ? (
                      <Doughnut data={doughnut} />
                    ) : (
                      <h2> No file distribution to display yet </h2>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
