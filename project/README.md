# Automation
Let Code generate Code

## 安装与使用说明

 ### 安装
 目前暂时推荐使用开发者模式来安装.
 1. clone 本项目.
 2. 在目录下执行 `sudo python setup.py develop` 这样就可以在全局目录引用  automation了
 
 ### 使用
 整个生成脚本命令的调用, 我建议通过 Automator Service 来调用.
 1. 你可以直接将我创建好的 Automator Service 从 `Utils/Services` 目录拷贝到你机器的
 `~/Library/Services` 目录. 使用哪一个就拷贝哪一个,或者全部拷贝过去.
 
 2. 在 Xcode 右键 弹出菜单,选择  Service 就可以看到对应的服务了.


## 一: 从 API 到 Model
这里的目的是自动将 API 的返回转成 Model.
我以 微博 API 为例进行说明:
比如 微博中的用户对象. 其 API 返回 示例如下:

```json
{
                "id": 1404376560,
                "screen_name": "zaku",
                "name": "zaku",
                "province": "11",
                "city": "5",
                "location": "北京 朝阳区",
                "description": "人生五十年，乃如梦如幻；有生斯有死，壮士复何憾。",
                "url": "http://blog.sina.com.cn/zaku",
                "profile_image_url": "http://tp1.sinaimg.cn/1404376560/50/0/1",
                "domain": "zaku",
                "gender": "m",
                "followers_count": 1204,
                "friends_count": 447,
                "statuses_count": 2908,
                "favourites_count": 0,
                "created_at": "Fri Aug 28 00:00:00 +0800 2009",
                "following": false,
                "allow_all_act_msg": false,
                "remark": "",
                "geo_enabled": true,
                "verified": false,
                "allow_all_comment": true,
                "avatar_large": "http://tp1.sinaimg.cn/1404376560/180/0/1",
                "verified_reason": "",
                "follow_me": false,
                "online_status": 0,
                "bi_followers_count": 215
            }
```
像这样的 API 返回 结果 , 我们在 应用中 创建一个 User 类,然后根据返回. 一个一个写上.
如:

```swift
struct User{
     let id:Int
     let screenName: String
    /// 省略
}
```
写这样的代码就像是做苦力一样. 为此, 我写了一个代码生成脚本. 能够快速的
从  API 生成模型代码.

先来看一发动图, 感受下 从 API 到 Model 是多么的方便.
[![Json2FieldsToModel](./Screenshots/json2fields_and_generate_model.gif)

**使用的是通过 Automator 创建系统服务的方式来调用脚本**

首先执行 将  json 转成 fields ,通过 json_to_fields() 函数 .得到结果如下:
上面是原来的  JSON 的. 以注释的形式保存. 下面是得到的字段列表.
```
/// {
/// "id": 1404376560,
/// "screen_name": "zaku",
/// "name": "zaku",
/// "province": "11",
/// "city": "5",
/// "location": "北京 朝阳区",
/// "description": "人生五十年，乃如梦如幻；有生斯有死，壮士复何憾。",
/// "url": "http://blog.sina.com.cn/zaku",
/// "profile_image_url": "http://tp1.sinaimg.cn/1404376560/50/0/1",
/// "domain": "zaku",
/// "gender": "m",
/// "followers_count": 1204,
/// "friends_count": 447,
/// "statuses_count": 2908,
/// "favourites_count": 0,
/// "created_at": "Fri Aug 28 00:00:00 +0800 2009",
/// "following": false,
/// "allow_all_act_msg": false,
/// "remark": "",
/// "geo_enabled": true,
/// "verified": false,
/// "allow_all_comment": true,
/// "avatar_large": "http://tp1.sinaimg.cn/1404376560/180/0/1",
/// "verified_reason": "",
/// "follow_me": false,
/// "online_status": 0,
/// "bi_followers_count": 215
/// }
id:d;screen_name;name;province;city;location;description;url:u;profile_image_url:u;domain;gender;followers_count:i;friends_count:i;statuses_count:i;favourites_count:i;created_at;following:i;allow_all_act_msg:i;remark;geo_enabled:i;verified:i;allow_all_comment:i;avatar_large:u;verified_reason;follow_me:i;online_status:i;bi_followers_count:i
```

### 通过字段列表的速写, 生成 Model 类型
将字段列表稍微分一下行, 如下.
```
id:d;screen_name;name;province;city;location;description;url:u;profile_image_url:u
domain;gender;followers_count:i;friends_count:i;statuses_count:i;favourites_count:i
created_at;following:i;allow_all_act_msg:i;remark;geo_enabled:i;verified:i;allow_all_comment:i
avatar_large:u;verified_reason;follow_me:i;online_status:i;bi_followers_count:i
```

字段简写的形式是 `filedName[:fieldType]` 各个字段声明以分号分隔开. `fieldType` 可以省略,省略则表示为 `String` 类型.
其他的字段简写说明:
- **`i`** : `Int`
- **`b`** : `Bool`
- **`d`** : `Double`
- **`s`** : `String` 如果是 String 类型的话,建议不用写,因为这是默认类型.
- **`u`** : `URL` 类型.
- **`j`** : `JSON` 类型.

其他更多类型支持,参见: 代码中 `ios_code_generator/maps.py:203` 的说明.


然后通过 ,字段名称及类型简写列表生成  Model.
这里假定 JSON 序列化库为 SwiftyJSON
为上模型名称及相应的配置 `User(eq,hash)`, 配置的意思看生成结果应该一目了然.

```
User(eq,hash)
id:d;screen_name;name;province;city;location;description;url:u;profile_image_url:u;domain;gender;followers_count:i;friends_count:i;statuses_count:i;favourites_count:i;created_at;following:i;allow_all_act_msg:i;remark;geo_enabled:i;verified:i;allow_all_comment:i;avatar_large:u;verified_reason;follow_me:i;online_status:i;bi_followers_count:i
```

生成出来的代码如下:

```swift
import SwiftyJSON
import BXModel
  struct User :BXModel{
    let id : Int
    let screenName : String
    let name : String
    let province : String
    let city : String
    let location : String
    let description : String
    let url : URL
    let profileImageUrl : URL
    let domain : String
    let gender : String
    let followersCount : Int
    let friendsCount : Int
    let statusesCount : Int
    let favouritesCount : Int
    let createdAt : String
    let following : Bool
    let allowAllActMsg : Bool
    let remark : String
    let geoEnabled : Bool
    let verified : Bool
    let allowAllComment : Bool
    let avatarLarge : URL
    let verifiedReason : String
    let followMe : Bool
    let onlineStatus : Int
    let biFollowersCount : Int

  init(json:JSON){
    self.id =  json["id"].intValue
    self.screenName =  json["screen_name"].stringValue
    self.name =  json["name"].stringValue
    self.province =  json["province"].stringValue
    self.city =  json["city"].stringValue
    self.location =  json["location"].stringValue
    self.description =  json["description"].stringValue
    self.url =  json["url"].stringValue.quietUrl
    self.profileImageUrl =  json["profile_image_url"].stringValue.quietUrl
    self.domain =  json["domain"].stringValue
    self.gender =  json["gender"].stringValue
    self.followersCount =  json["followers_count"].intValue
    self.friendsCount =  json["friends_count"].intValue
    self.statusesCount =  json["statuses_count"].intValue
    self.favouritesCount =  json["favourites_count"].intValue
    self.createdAt =  json["created_at"].stringValue
    self.following =  json["following"].boolValue
    self.allowAllActMsg =  json["allow_all_act_msg"].boolValue
    self.remark =  json["remark"].stringValue
    self.geoEnabled =  json["geo_enabled"].boolValue
    self.verified =  json["verified"].boolValue
    self.allowAllComment =  json["allow_all_comment"].boolValue
    self.avatarLarge =  json["avatar_large"].stringValue.quietUrl
    self.verifiedReason =  json["verified_reason"].stringValue
    self.followMe =  json["follow_me"].boolValue
    self.onlineStatus =  json["online_status"].intValue
    self.biFollowersCount =  json["bi_followers_count"].intValue
}

  func toDict() -> [String:Any]{
var dict : [String:Any] = [ : ]
    dict["id"] = self.id
    dict["screen_name"] = self.screenName
    dict["name"] = self.name
    dict["province"] = self.province
    dict["city"] = self.city
    dict["location"] = self.location
    dict["description"] = self.description
    dict["url"] = self.url.absoluteString
    dict["profile_image_url"] = self.profileImageUrl.absoluteString
    dict["domain"] = self.domain
    dict["gender"] = self.gender
    dict["followers_count"] = self.followersCount
    dict["friends_count"] = self.friendsCount
    dict["statuses_count"] = self.statusesCount
    dict["favourites_count"] = self.favouritesCount
    dict["created_at"] = self.createdAt
    dict["following"] = self.following
    dict["allow_all_act_msg"] = self.allowAllActMsg
    dict["remark"] = self.remark
    dict["geo_enabled"] = self.geoEnabled
    dict["verified"] = self.verified
    dict["allow_all_comment"] = self.allowAllComment
    dict["avatar_large"] = self.avatarLarge.absoluteString
    dict["verified_reason"] = self.verifiedReason
    dict["follow_me"] = self.followMe
    dict["online_status"] = self.onlineStatus
    dict["bi_followers_count"] = self.biFollowersCount
return dict
}
}

    extension User: Equatable{
         static func ==(lhs:User,rhs:User) -> Bool{
        return lhs.id == rhs.id
        }
    }



    extension  User : Hashable{
      var hashValue:Int{ return id.hashValue   }
    }

```



## Enum 好用, Enum 可以更易用
Swift 3 中的枚举可以说是我,好用到让我惊讶的程度.
但是我可以让它更易用.

### 经典用例
比如 用它来封装 应用 微信的 Tab 栏枚举,如下:

```swift
enum AppTab{
    case wechat,contacts,discover,me
}
```
到这里已经比用整型常量好很多了.
好了,现在你想将 UITabBarItem 中的构造封装在里面.
1. 首先我们为其添加一个 `title` 属性,如下:

```swift
extension AppTab{
  var title:String{
    switch self {
    case .wechat: return "微信"
    case .contacts: return "通讯录"
    case .discover: return "发现"
    case .me: return "我"
    }
  }
}

```

然后.就可以直接使用 `.title` 就可以访问了. 避免了 使用字典保存映射的麻烦. 写法,修改也简单.

2. 你想判断某一个 AppTab 值是不是 me.
 你选择这样做 ` if tab == .wechat` 嗯, Swift 中可以直接写 `.wechat` 这样的枚举值真方便.
 但是你也可以这样. 添加一个 Bool 类型的 Computed Property.
 
```swift
extension AppTab{
  var isWechat:Bool{ return self == .wechat }
}
```

然后你想为所有的枚举值都加上这样的 Computed Property. 你复制粘贴然后修改.


3. 很多时候,你想遍历枚举值, 于是你添加了一个静态属性.保存所以的枚举值为一个数组.
如下:

```swift
extension AppTab{
  static let allCases:[ AppTab] = [.wechat, .contacts, .discover, .me]
}
```

### 动起来

so far, so good. 那我可以帮到你什么呢? 我可以帮你少写代码.
怎么帮?

1. 只需要写少量的几行声明:

如下.
```
AppTab
wechat:微信
contacts: 通讯录
discover:发现
me:我
```
选中, 右键, 选择 "Services|generate_enum"
然后如下代码就自动生成了:

```swift
//AppTab
//wechat:微信
//contacts: 通讯录
//discover:发现
//me:我
enum AppTab  {
     case wechat, contacts,discover,me
    var isWechat:Bool{ return self == .wechat }
    var isContacts:Bool{ return self == .contacts }
    var isDiscover:Bool{ return self == .discover }
    var isMe:Bool{  return self == .me }
    var title:String{
        switch self{
        case .wechat:return "微信"
        case .contacts:return " 通讯录"
        case .discover:return "发现"
        case .me:return "我"
        }
    }
    static let allCases:[AppTab] = [.wechat,.contacts,.discover,.me]
}
```

怎么样? 来试试吧!
当然还有其他选项可以使用. 如果你有其他需要麻烦告诉我. 当然有 PR 最好了.

最后来张动图感受一下:

![Generate Enum](Screenshots/generate_enum.gif)

## 生成偏好设置访问存取代码
![Generate Settings](Screenshots/generate_settings.gif)

## 未完待续
项目其他生成脚本的使用说明,稍后更新.
