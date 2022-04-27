package emotion.mapper;

import emotion.po.StaffEvaluation;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@Transactional
public class StaffEvaluationMapperTest {
    @Autowired
    private StaffEvaluationMapper staffEvaluationMapper;

    @Test
    public void testGetLatestStaffEvaluation() throws Exception{
        StaffEvaluation staffEvaluation = staffEvaluationMapper.getLatestStaffEvaluation(172L);
        System.out.println(staffEvaluation.getScore());
    }
}
