package web3.example;

import java.math.BigInteger;

import org.junit.jupiter.api.Test;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.DefaultGasProvider;

import web3.beaglegaze.example.UsageContract_sol_UsageContract;

public class FundTest {

    @Test
    void fund() throws Exception {
        Web3j web3j = Web3j.build(new HttpService("http://localhost:8545"));
        Credentials credentials = Credentials
                .create("0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc");
        UsageContract_sol_UsageContract contract = UsageContract_sol_UsageContract.load(
                "0x289B72CEeaB48832261626D62E3daA87Fd90B024",
                web3j,
                credentials,
                new DefaultGasProvider());
        org.web3j.protocol.core.methods.response.TransactionReceipt response = contract
                .fund(BigInteger.valueOf(2000)).send();
        System.out.println("Transaction hash: " + response.getTransactionHash());
    }
}
