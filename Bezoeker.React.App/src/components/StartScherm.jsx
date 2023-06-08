import React from 'react';
import { Link } from 'react-router-dom';
import Header from './header';

const StartScherm = () => {
  return (
    <>
    <div className="flex h-screen justify-center items-end">
      <Header />
      <div className="text-center mb-60">
        <Link to="/aankomst" className="btn btn-primary btn-lg px-4 py-2">
          Ik kom aan
        </Link>
        <div className='p-3'></div>
        <Link to="/vertrek" className="btn btn-primary btn-lg px-4 py-2">
          Ik vertrek
        </Link>
      </div>
    </div>
    </>
  );
};

export default StartScherm;
