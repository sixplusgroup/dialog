package emotion.mapper;

import emotion.po.CaseEvaluation;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@SpringBootTest
@Transactional
public class CaseEvaluationMapperTest {
    @Autowired
    private CaseEvaluationMapper caseEvaluationMapper;

    @Test
    public void testGetAllCaseEvaluations() throws Exception{
        List<CaseEvaluation> caseEvaluations = caseEvaluationMapper.getAllCaseEvaluations();
        for(CaseEvaluation caseEvaluation:caseEvaluations)
            System.out.println(caseEvaluation.getName());
    }
}
