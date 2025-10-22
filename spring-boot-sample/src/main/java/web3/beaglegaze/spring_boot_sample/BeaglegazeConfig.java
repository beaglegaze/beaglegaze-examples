package web3.beaglegaze.spring_boot_sample;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;
import web3.beaglegaze.AsyncBatchProcessor;
import web3.beaglegaze.BatchMode;
import web3.beaglegaze.ContractConsumer;
import web3.beaglegaze.MicroPaymentAspect;
import web3.beaglegaze.SmartContract;

@Configuration
public class BeaglegazeConfig {


    @Value("${beaglegaze.account.private-key}")
    private String accountPrivateKey;

    /**
     * Here we initialize Beaglegaze. We need to set our Smart Contract Address, the
     * ethereum node URL,
     * and the private key of the account that will be used to pay for the calls (provided by the client deploying the software).
     * 
     * The Smart Contract address points to the Smart Contract that was deployed to manage the pay-per-call payments.+
     * The flow typically is as follows:
     * 1. The developers deploy the beaglegaze smart contract, 
     * 2. they hard-code the contract address into their software (as we do here),
     * 3. clients deploying the software provide their own ethereum account private key to be used for payments,
     * 4. the client's account is charged when the endpoints are called.
     * 
     * @throws Exception
     */
    @PostConstruct
    public void init() throws Exception {
        AsyncBatchProcessor asyncBatchProcessor = new AsyncBatchProcessor(BatchMode.OFF);
        asyncBatchProcessor.addObserver(new ContractConsumer(
                new SmartContract("0x289B72CEeaB48832261626D62E3daA87Fd90B024", "http://localhost:8545",
                        accountPrivateKey, 1000)));
        MicroPaymentAspect.setProcessor(asyncBatchProcessor);
    }

}
