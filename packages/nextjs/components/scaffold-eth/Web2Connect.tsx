"use client";

import { createThirdwebClient } from "thirdweb";
import { base, baseSepolia } from "thirdweb/chains";
import { ConnectButton } from "thirdweb/react";
import { createWallet, inAppWallet } from "thirdweb/wallets";

console.log("base:", base, baseSepolia);

const wallets = [inAppWallet(), createWallet("io.metamask"), createWallet("com.coinbase.wallet")];

const client = createThirdwebClient({
  clientId: process.env.NEXT_PUBLIC_THIRDWEB_SECRET_KEY as string,
});

// console.log("client:", client, wallets);

export const Web2Connect = () => {
  return (
    <ConnectButton
      client={client}
      wallets={wallets}
      accountAbstraction={{
        chain: baseSepolia,
        sponsorGas: true,
      }}
    />
  );
};
