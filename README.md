# Stafla
## Notendasaga (40%)

### Hvað er Stafla?
Stafla er kerfi sem hjalpar þer að setja saman afnanga og finna þæginlegustu leiðirnar fyrir þig til að útskrifast úr skólanum, Það er hægt að velja a milli þæginlegustu leiðina, vinsælustu leiðina eða leiðina sem hentar þér best eftir framhaldsskóla.

### Til hvers er Stafla áætlað?
Stafla er áætluð fyrir nemendur og Stafla setur saman áfangana fyrir þig og gefur þér upplýsingar um þá áfanga, og margar mismundandi leiðir til að klara áfangana, hvort að þu viljir taka einhver áfanga á fyrstu eða fjórðu önninni þinni, Stafla getur gert það allt.

**_hún getur einnig verið notuð fyrir kennara til að finna leiðir fyrir nemendur (SEINNA)_**

### Afhverju mundi fólk vilja nota Stöflu?
Afþvi maður sjálfur og eflaust fullt af nemendum hafa lent í þvi að eithvað varðandi stundatöflunnar fer úrskeðis, hvort að það séu fullt af árekstrum eða eithvað sem hentar þér bara alls ekki, Stafla mun vonandi minnka þessi mistök, og gera áfanga valið þitt og lífið þitt í skólanum einfaldara og þæginlegra.

## Útskýring á virkni vefsíðu

### Heimasíða
Á heimasiðunni verður hægt að velja skóla og brautinna sem þú ert í til að byrja afanga valið þitt. það verður **LogIn/SignIn** líka á siðunni. Svo verður **contact us** takki sem verður notaður til að láta okkur vita ef það er eithvað á síðunni sem virkar ekki, svo er lika hægt að nota hann fyrir spurningar til okkar.
### Námsmats tafla
Hérna mun Stafla sýna þér eftir síum bestu áfanga sem eru til að taka og gefur valmöguleika til að skoða áfangalýsingar og áfangana sem Stafla sýndi þér og ef skal þurfa þá er hægt að breyta þeim áföngum sem Stafla valdi fyrir þig.

### Sign up & Sign in
Það er hægt að búa til account til að geta vistað námsmats töflu sína og nálgast hennar seinna.

### Admin dashboard
Á Admin dashboardinu er hægt að búa til eða breyta skóla/brautir/áföngum sem nemendar geta svo valið til að stilla upp sína eigin námsmats töflu.


---


## Wireflows (Wireframes + flowchart + User story) (60%)
![Wireframe](https://github.com/vefthroun4/Stafla/blob/main/wireframe_vefthr4.svg)

## [Screenshots](https://github.com/vefthroun4/Stafla/tree/main/Screenshots)

## [Youtube](https://youtu.be/3vAFwBt4zrY)

### Network
![Network image](https://github.com/vefthroun4/Stafla/blob/main/Screenshots/network.png)

[Projects](https://github.com/orgs/vefthroun4/projects/2/views/1)

## Frameworks og Söfn:
### Flask
Frameworkið sem við notuðum.

### Migrate
Notað til að uppfæra gagnagrunnin þegar breytingar voru framkvæmdar á Models í sqlalchemy

### sqlalchemy
Gagnagrunnurinn sem notaður var, notaði SQLITE fyrir development en POSTGRESQL fyrir production

### flask-wtf, wtf-sqlalchemy og wtforms
Þrjú mismunandi söfn fyrir forms, eitt sérstaklega þannig að queries gæti verið framkvæmdar á runtime þegar er verið að smíða formið og hinn tvö bara fyrir almena virkni á forms

### flask-login
notað fyrir auðkenningu, vinnur mjög vel með sqlalchemy.

### Framendi
notað var semantic-ui


# Gagnagrunnshönnun
Gagnagrunnurinn var sú flókknasta atriði að útfæra í þessu verkefni. Það eru 12 töflur(e. Tables) í honum og 10 þeirra aðeins fyrir að halda utan um gögninn tengd námsmats töflunni. 
![mynd](https://github.com/vefthroun4/Stafla/blob/main/Screenshots/database.png)

## útskýring á Tables

### User og Roles
User taflan heldur utan um notenda og Roles er aðeins fyrir aðgángstýringu, t.d. hvort hann sé anonymous, user eða admin.

### Schools, Divisions og Tracks
Schools, Divisions og Tracks eru Skólar, undirskólar og brautir, þessar upplýsingar voru grunnupplýsingarnar sem námsmatstaflan mundi byggja upp á, þessar töflur tengjast öðrum töflum með ForeignKey(FK), þessar upplýsingar gera samt ekki neit þangað til að þær eru tengdar við aðrar töflur í gagnagrunninn.

### (Courses, Prerequisites), TrackCourses og CourseGroups
Courses eru bara allir áfangar sem eru í gagnagrunninn og TrackCourse tengir einhvern af þeim áfanga með FK og Course er bættur í TrackCourses verður hann aðgengilegur að notendum til að vera valinn í gegnum námsmatstöflukerfið þegar viðeigandi Track(Braut) er valinn. annars heldur Prerequisites um undanfara og meiri segja framhalds áfanga af hverjum einasta áfanga í kerfinu og CourseGroups var smíðaður vegna áföngum sem voru kröfu áfangar en þurfti aðeins að klára t.d. 2 af 3 áföngum í það hópi t.d. eins og ÍSL3 áfangarnir á tölvubraut þar sem maður þarf aðeins að klára 2 of 3 áföngum í það hóp.

### UsersRegistration, (CourseRegistration og course_state)
UsersRegistration er til að skrá töflu á notenda, þannig hann getur valið Skóla, undirskóla og braut og svo gegnum CourseRegistration er hægt að skrá áfangana í UsersRegistration sem svo heldur utan um hvaða önn þeir voru skráðir hversu marga áfanga hefur nemandi hefur tekið, og svo er course_state einfaldlega til að breyta stöðu skráðan áfanga, t.d. notandi fellur á STÆ áfanga þá er hægt að merkja hann sem FAILED og svo er líka hægt að merkja hann sem ACTIVE, FINISHED. Það var haldinn utam um þessa statusa í States töflunna í [models.py línu 287](https://github.com/vefthroun4/Stafla/blob/main/app/models.py#L287)

## Vandamál með gagnagrunn
Að læra á MYSQLALCHEMY var mjög stórt vesen þar sem það nýtur sér Object-relational mapping, sem í stuttu þýðir að í staðinn fyrir að nota töflur þá er notaða python klassa sem erfða frá mysqlalchemy.model sem er í raun og veru bara Declarative Base, þetta þýðir að syntaxið fyrir mysql fyrirspurnir voru talsvert öðruvísi og í raun og veru flokknari en þegar það var set up á réttan hátt var hægt að gera mjög flóknar fyrirspurnir með því að aðeins kalla í einn attribute(e. Column) sem er tengdur öðrum töflum með svokölluðu Relationship sem framkvæmir þessar flóknar joins. 

Annað stórt vandamál var joins, allar töflur eru tengdar saman með joins og það eru til mjög margar loading-strategies sem eru áætlaðar að optimisea queries og joins og svo þurfti stundum að búa til custom joins, t.d. til að ná í alla áfanga sem nemandi hafði ekki ljúkið við til að sýna honum alla mögulega áfanga sem hann getur valið, (ath. þetta var útfært í gegnum API´Ð en ekki notað vegna ekki náðist að útfæra námsmatstöfluna.)



## Næstu skref
1. Fyrst og fremmst væri það að koma námsmats töfluni til að virka almennilega, þannig að það útfærir áfanga fyrir nemanda og leyfir nemanda að breyti því til að fá einhverja ákveðna töflu eftir þörfum.
1. Útfæra profile fyrir notanda þannig að notandinn gæti breytt sínum upplýsingum. 
1. Klára api þannig að hægt er að nota AJAX(J) í staðinn fyrir að endurhlaða síðuna hvert sinn gögninn eru uppfært eða sótt með formi.
1. Admin dashboard þar sem þeir með Moderator réttindi eða hærri gæta bætt við fleiri gögnum á síðuna og hægt að breyta öllum gögnum sem eru til í gagnagrunninum sem það notandi hafði rétt að.
1. Lagfæra kóðan, gefa betri villuboð, gera aðgangstýringuna betri, o.s.fr.


# Höfundar: Elvar Ágúst, Fuad Poroshtica, Sveinn Óli, Karl Philip
