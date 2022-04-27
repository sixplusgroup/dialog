package emotion.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import emotion.po.StaffEvaluation;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StaffEvaluationMapper extends BaseMapper<StaffEvaluation>{
    @Select("select * from staff_evaluation where staff_id = #{staffId} order by id desc limit 1")
    StaffEvaluation getLatestStaffEvaluation(Long staffId);

    @Select("select * from staff_evaluation where staff_id = #{staffId}")
    List<StaffEvaluation> getStaffEvaluations(Long staffId);
}
