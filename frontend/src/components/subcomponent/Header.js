import FileForm from "./FileForm";
import { Link } from "react-router-dom";

const Header = ({ profile, setData, parentId }) => (
  <header className="d-flex align-items-center justify-content-center">
    <div className="d-flex align-items-center justify-content-center w-50 bg-light border rounded-bottom">
      <div>
        <Link to="/">
          <img className="prof-image" src={profile.picture} alt="" />
        </Link>
      </div>
      <div className="align-self-baseline m-1">
        <h5>
          Fullname:
          <strong>
            {profile.first_name} {profile.last_name}
          </strong>
        </h5>
        <div className="align-self-start">
          <FileForm parentId={parentId} setData={setData} />
        </div>
      </div>
    </div>
  </header>
);

export default Header;
