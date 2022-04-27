package emotion.service;


import emotion.po.CaseEvaluation;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;

@SpringBootTest
@Transactional
public class CaseServiceTest {
    @Autowired
    private CaseService caseService;

    @Test
    public void testGetTypicalCases() throws Exception{
        Map<String, List<CaseEvaluation>> typicalCases = caseService.getTypicalCases();
        typicalCases.forEach((key,value)->{
            System.out.println(key);
            for(CaseEvaluation caseEvaluation:value)
                System.out.println(caseEvaluation.getName());
        });
    }

    @Test
    public void testGetCaseLoudness() throws Exception{
        List<double[]> caseLoudnessPairs = caseService.getCaseLoudnessPairs("153358957970214090718866",172L);
        for(double[] pair:caseLoudnessPairs){
            System.out.println(pair[0]);
            System.out.println(pair[1]);
        }
    }
}
