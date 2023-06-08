import React, { useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';

const EindSucces = () => {
  const history = useHistory();

  useEffect(() => {
    const timer = setTimeout(() => {
      history.push('/');
    }, 5000);

    return () => clearTimeout(timer);
  }, [history]);

  return (
    <div className="heading text-center mt-4">
      <h1>Bedankt voor uw bezoek!</h1>
    </div>
  );
};

export default EindSucces;
