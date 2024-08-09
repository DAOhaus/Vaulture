"use client";

// import { Address } from "viem";
// import { useTargetNetwork } from "~~/hooks/scaffold-eth/useTargetNetwork";
// import { useGlobalState } from "~~/services/store/store";
import { createThirdwebClient } from "thirdweb";
import { baseSepolia } from "thirdweb/chains";
import { inAppWallet } from "thirdweb/wallets";

const wallet = inAppWallet({
  smartAccount: {
    chain: baseSepolia,
    sponsorGas: true,
  },
});
console.log("wallet:", wallet, process.env.THI);

const client = createThirdwebClient({
  clientId: process.env.NEXT_PUBLIC_THIRDWEB_SECRET_KEY as string,
});
console.log("client:", client);

const handleConnect = async () => {
  const account = await wallet.connect({
    client,
    chain: baseSepolia,
    strategy: "google",
  });
  console.log("account:", account);
};

// type Web2ConnectProps = {
//   address?: Address;
//   className?: string;
//   usdMode?: boolean;
// };

/**
 * Display (ETH & USD) balance of an ETH address.
 */
// export const Web2Connect = ({ address, className = "", usdMode }: Web2ConnectProps) => {
export const Web2Connect = () => {
  // const { targetNetwork } = useTargetNetwork();
  // const nativeCurrencyPrice = useGlobalState(state => state.nativeCurrency.price);
  // const isNativeCurrencyPriceFetching = useGlobalState(state => state.nativeCurrency.isFetching);

  return <div onClick={handleConnect}>connect</div>;
};
