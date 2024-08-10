"use client";

import { createThirdwebClient } from "thirdweb";
import { sepolia } from "thirdweb/chains";
import { ConnectButton, PayEmbed } from "thirdweb/react";
import { createWallet, inAppWallet } from "thirdweb/wallets";

const wallets = [
  inAppWallet({
    auth: {
      options: ["email", "google", "phone", "passkey"],
    },
  }),
  createWallet("io.metamask"),
  createWallet("com.coinbase.wallet"),
];

const client = createThirdwebClient({
  clientId: process.env.NEXT_PUBLIC_THIRDWEB_SECRET_KEY as string,
});

export const Web2Connect = () => {
  return (
    <div>
      <ConnectButton
        client={client}
        wallets={wallets}
        accountAbstraction={{
          chain: sepolia,
          // factoryAddress: "YOUR_FACTORY_ADDRESS",
          gasless: true,
        }}
        theme={"dark"}
        connectModal={{ size: "compact" }}
      />
    </div>
  );
};

export const PayWidget = () => {
  return <PayEmbed client={client} />;
};
