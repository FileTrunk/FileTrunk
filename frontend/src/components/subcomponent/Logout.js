import Cookies from 'universal-cookie';

const Logout = ({ setIfAuthorized }) => {
  const logOut = () => {
    const cookies = new Cookies();
    cookies.remove('jwt');
    setIfAuthorized(false);
  };
  return (
    <button className="m-t-10 waves-effect waves-dark btn btn-primary btn-md btn-rounded" onClick={() => { logOut(); }}>Logout</button>
  );
};

export default Logout;
