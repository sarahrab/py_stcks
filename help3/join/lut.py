class LUTypeModel(SQLModel, table=True):
    __tablename__ = "TBL_LU_TYPES"

    lu_type_id: Optional[int] = Field(default=None, primary_key=True)
    lu_type_name: Optional[str] = Field(default=None)

class LUValueModel(SQLModel, table=True):
    __tablename__ = "TBL_LU_VALUES"

    lu_value_id:  Optional[int] = Field(default=None, primary_key=True)
    lu_type_id: Optional[int] = Field(default=None)
    lu_code: Optional[int] = Field(default=None)
    lu_value: Optional[str] = Field(default=None)

# TBL_LU_TYPES:
# 1: "Roles"
# 2: "RequestStatus"
# 3: "ErrorType"

# TBL_LU_VALUES:
# 1, 1, 1, "Admin"
# 2, 1, 2, "Regular"
# 3, 2, 1, "Pending"
# 4, 2, 2, "Canceled"
# 5, 2, 3, "Processed"

class Role(Enum):
    Admin = 1
    Regular = 2


class UserAccountFull(BaseModel):
    user_id: int | None = Field(default=None, primary_key=True)
    user_name: str | None
    amount: int | None
    is_logged_in: bool | None = Field(default=False)
    level: Optional[Role] = Role.Admin
    role: Optional[str]


def get_user_data(user_id: int) -> UserAccountFull | None:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(UserModel, LUValueModel).where(UserModel.user_id == user_id).join(LUValueModel, cast(ColumnElement, LUValueModel.lu_code == UserModel.level and LUValueModel.lu_type_id == 1))
            user = session.exec(st).one_or_none()
            if user:
                result = UserAccountFull(user_id = user[0].user_id, name =user[0].name,  amount =user[0].amount,
                                         level =Role(user[0].level), role = user[1].lu_value)
                return result

    except Exception as ex:
        return None
