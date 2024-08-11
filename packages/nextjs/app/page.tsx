"use client";

import type { NextPage } from "next";
import { PayWidget } from "~~/components/scaffold-eth";

const Home: NextPage = () => {
  return (
    <>
      <div className="flex items-center flex-col flex-grow pt-10">
        <div className="px-5">
          <h1 className="text-center">
            <span className="block text-4xl font-bold">Vaulture</span>
          </h1>
          <div className="flex justify-center items-center space-x-2 flex-col sm:flex-row mb-4">
            <p className="my-2 font-medium">Purchase Tokens to deposit Into Vault</p>
          </div>
          <PayWidget />
          <div className="btn btn-success w-full mt-4">Withdraw</div>
        </div>
      </div>
    </>
  );
};

export default Home;
