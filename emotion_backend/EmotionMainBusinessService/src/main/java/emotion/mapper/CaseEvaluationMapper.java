package emotion.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import emotion.po.CaseEvaluation;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CaseEvaluationMapper extends BaseMapper<CaseEvaluation> {
    @Select("Select * from case_evaluation")
    List<CaseEvaluation> getAllCaseEvaluations();

    @Select("Select * from case_evaluation where name=#{caseName} and staff_id=#{staffId}")
    CaseEvaluation getByCaseNameAndStaffId(String caseName,Long staffId);

    @Select("Select * from case_evaluation where staff_id=#{staffId}")
    List<CaseEvaluation> getByStaffId(Long staffId);
}
