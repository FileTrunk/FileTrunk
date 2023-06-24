import Cookies from 'universal-cookie';

const getJWT = () => {
  const cookies = new Cookies();
  return cookies.get('jwt');
};

export default getJWT;
