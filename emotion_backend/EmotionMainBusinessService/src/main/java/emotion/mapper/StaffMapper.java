package emotion.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import emotion.po.Staff;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StaffMapper extends BaseMapper<Staff>{
    @Select("select * from staff")
    List<Staff> getAllStaffs();
}
