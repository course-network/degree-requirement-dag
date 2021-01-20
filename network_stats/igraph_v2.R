
library(dplyr)
library(igraph)


# reqs <- read.csv("./parse_course_requirements/edges.csv", header = F)
reqs <- read.csv("./convert_database_format/edges.csv", header = F)
#  Using this file locally until we merge branches.


head(reqs)
names(reqs) <- c("pre_rec", "course")


req_net <- graph_from_data_frame(reqs, directed = T)
plot(req_net, directed = T)
tree_layout <- layout.reingold.tilford(req_net, root = "ST 623", circular = FALSE, flip.y = FALSE)


# stat <- stat %>% select(ref, course, pre_rec, name)
# names(reqs) <- c("course", "ref", "pre_rec", "name")
# stat <- stat %>% select(ref, course, pre_rec, name)
# st_net <- graph_from_data_frame(stat, directed = T)
# plot(st_net)

st_net <- graph_from_data_frame(stat, directed = T)
plot(st_net)
plot(st_net, edge.color = stat$pre_rec, edge.curved = 0.3, edge.width = 2) # Thicker lines

# Calculate node degree
degree(st_net)
plot(st_net, vertex.color = degree(st_net))





# Counting dependencies ------------------------------

# Pre requisite department (academic unit)
reqs$pre_dept <- sub(x = reqs$pre_rec,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# There are about half of pre-requisites that
#  were in-department.
table(reqs$pre_dept == reqs$course_dept)

reqs$pre_dept[reqs$pre_dept == "NE"] <- "NSE"
# Count number of dependencies.
reqs %>% filter(pre_dept != "of") %>%
  group_by(pre_dept) %>%
  summarise(n = n()) %>% arrange(desc(n))

# Count number of
# Nuclear science got changed to NSE.
reqs$pre_dept[reqs$pre_dept == "NE"] <- "NSE"
reqs %>% filter(pre_dept != "and", pre_dept != "or", pre_dept != "of", pre_dept != course_dept) %>%
  group_by(pre_dept) %>%
  summarise(n = n()) %>% arrange(desc(n))


# This is going to require some trickery to pass the OR nodes through as pre-requisites.
#  Maybe they shoudn't count at full weight if they're an OR?
#  Count it proportional to the number of elements in the OR maybe?


# reqs$pre_dept[reqs$pre_dept == "NE"] <- "NSE"
# External pre-requisites
reqs %>% filter(pre_dept != course_dept) %>%
  group_by(pre_dept) %>% filter(pre_dept != "OR") %>%
  summarise(n = n()) %>% arrange(desc(n))

reqs %>%
  group_by(pre_dept) %>% filter(pre_dept != "OR") %>%
  summarise(n = n()) %>% arrange(desc(n))



# Create a small plot, math meets CS ------------------------------
# This will require the OR node data.
reqs$pre_dept <- sub(x = reqs$pre_rec,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course,
                        pattern = "([A-z]+) .+",
                        replacement = "\\1")

sub_reqs <- reqs %>% filter(pre_dept %in% c("MTH", "CS") | course_dept %in% c("MTH", "CS")) %>% head(100)

sub_net <- graph_from_data_frame(sub_reqs, directed = T)


sub_reqs$or <- 1 + 1*(sub_reqs$course_dept == "OR")
sub_reqs$or_color <- c("grey", "steelblue")[sub_reqs$or]
plot(sub_net, directed = T, edge.color = sub_reqs$or, vertex.size = 2)

# Full graph with character expand smaller.
reqs$or <- 1 + 1*(reqs$course_dept == "OR")
full_net <- graph_from_data_frame(reqs, directed = T)
plot(sub_net, directed = T, edge.color = reqs$or, vertex.size = 2, arrow.width = 0.5, label.cex = 5)

V(sub_net)$label.cex = 0.65
V(sub_net)$arrow.size = 0.2
E(sub_net)$edge.color = sub_reqs$or_color
V(sub_net)$vertex.size = 1
plot.igraph(sub_net)





# The most popular course ------------------------------
head(reqs)

# This will require the OR node data.
reqs$pre_dept <- sub(x = reqs$pre_rec,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course,
                        pattern = "([A-z]+) .+",
                        replacement = "\\1")

# Some OR nodes have a lot of options.
top10 <- reqs %>% filter(course_dept == "OR") %>%
  group_by(course) %>% summarise(n_pr = n()) %>% arrange(desc(n_pr)) %>% head(10)

library(pander)
pander(left_join(top10, reqs, by = c("course" = "pre_rec")))


reqs %>% filter(course_dept != "OR") %>%
  group_by(course) %>% summarise(n_pr = n()) %>% arrange(desc(n_pr)) %>% head(10)




sub_reqs <- reqs %>% filter(pre_dept %in% c("MTH", "CS") | course_dept %in% c("MTH", "CS")) %>% head(100)




# Distribution of number of pre-requisites:
# X courses have no pre-requisite.

# ALS courses ------------------------------
# Color, size, and shape working out.

reqs <- read.csv("./convert_database_format/edges.csv", header = F)

names(reqs) <- c("pre_rec", "course")

# This will require the OR node data.
reqs$pre_dept <- sub(x = reqs$pre_rec,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course,
                        pattern = "([A-z]+) .+",
                        replacement = "\\1")

head(reqs)
dim(reqs)

# sub_reqs <- reqs %>% filter(pre_dept %in% c("MTH", "CS") | course_dept %in% c("MTH", "CS")) %>% head(100)
sub_reqs <- reqs %>% head(6)

courses <- c("ALS 151", "ALS 161", "ALS 162", "OR 0", "OR 1")
sub_reqs <- reqs %>% filter(pre_rec %in% courses | course %in% courses)
sub_reqs$or <- 1 + 1*(sub_reqs$course_dept == "OR")

sub_net <- graph_from_data_frame(sub_reqs, directed = T)
plot.igraph(sub_net)
plot(sub_net, directed = T,
     edge.color = sub_reqs$or,
     vertex.size = 12,
     vertex.shape = c("circle", "square")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1],
     vertex.color =  c("grey", "steelblue")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1])



# Might try with certain CS courses?

# sub_reqs <- reqs %>% filter(pre_dept %in% c("MTH", "CS") | course_dept %in% c("MTH", "CS"))

# Math oR CS
# sub_reqs <- reqs %>% filter(course_dept %in% c("MTH", "CS"))
head(reqs)
csor <- reqs$pre_rec[(reqs$pre_dept == "OR" & reqs$course_dept == "CS")]
reqs$csor <- reqs$course %in% csor
sum(reqs$csor)


sub_reqs <- reqs %>% filter(course_dept %in% c("CS") | csor)
sub_reqs$or <- 1 + 1*(sub_reqs$course_dept == "OR")

sub_net <- graph_from_data_frame(sub_reqs, directed = T)
plot.igraph(sub_net)
plot(sub_net, directed = T,
     edge.color = sub_reqs$or,
     vertex.size = 12,
     vertex.shape = c("circle", "square")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1],
     vertex.color =  c("grey", "steelblue")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1])


# Let's spread the points better
fr_net <- layout_nicely(sub_net)
plot(sub_net, layout = fr_net, directed = T,
     edge.color = sub_reqs$or,
     vertex.size = 5,
     vertex.shape = c("circle", "square")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1],
     vertex.color =  c("grey", "steelblue")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1])

# That's pretty good.

# Academic units feeding into CS, by number of pre-reqs used.
library(pander)
head(sub_reqs)
sub_reqs %>%
  filter(!(pre_dept %in% c("CS", "OR"))) %>%
  group_by(pre_dept) %>%
  summarise(n = n()) %>%
  arrange(desc(n)) %>%
  pander()

# Now lets scale by weighted in-degree.

# Out degree: the nubmer of pre_rec edges originating at that course.
#  We'll want to make the ones which are pre_req going to an OR fractional,
#   depending on the number of edges going into that.


head(sub_reqs)
sr_group <- sub_reqs %>% group_by(pre_rec) %>% summarise(n = n())
sr_n <- left_join(data.frame(names = names(V(sub_net))), sr_group, by = c("names" = "pre_rec"))
head(sr_n)
sr_n$n[is.na(sr_n$n)] <- 0

sr_layout <- layout_nicely(sub_net)
plot(sub_net, directed = T,
     layout = sr_layout,
     edge.color = sub_reqs$or,
     vertex.size = sr_n$n * 1.5,
     vertex.shape = c("circle", "square")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1],
     vertex.color =  c("grey", "steelblue")[grepl(x = names(V(sub_net)), pattern = "OR.+") + 1])
